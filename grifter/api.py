import copy
import logging

from .validators import validate_schema

from .custom_filters import (
    explode_port,
)

from .loaders import (
    render_from_template,
    load_data,
)

from .constants import (
    TEMPLATES_DIR,
    BLACKHOLE_LOOPBACK_MAP,
    ALL_GUEST_DEFAULTS,
    GUEST_SCHEMA_FILE,
    GUESTS_SCHEMA_FILE,
    GUEST_DEFAULTS_DIRS,
)


custom_filters = [
    explode_port,
]

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(format='%(levelname)s - %(message)s')


def generate_loopbacks(guest_list=None, network='127.255.1'):
    """
    Generate a dict of loopback addresses
    :param guest_list: List of guests
    :param network: Network portion of the loopback addresses
    :return: Dictionary of loopback addresses
    """
    if guest_list is None or not isinstance(guest_list, list):
        raise AttributeError('guest_list should contain a list of guests')
    elif not guest_list:
        raise ValueError('list of guests is empty')

    guests = [i['name'] for i in guest_list]
    loopbacks = [f'{network}.{i}' for i in range(1, len(guests) + 1)]
    guest_to_loopback_map = dict(zip(guests, loopbacks))

    return {**guest_to_loopback_map, **BLACKHOLE_LOOPBACK_MAP}


def update_context(source, target):
    """
    Take a source dict and update it with target data
    :param source: Source data dictionary
    :param target: Target data dictionary to update
    :return: Return new dict with merged data
    """
    new_context = copy.deepcopy(target)
    for k, v in source.items():
        if k in target:
            if isinstance(target[k], dict):
                new_context[k].update(source[k])
            else:
                new_context[k] = source[k]

    return new_context


def load_guest_defaults(guest_defaults_file):
    """
    Load guest_defaults_file from the following locations top to
    bottom least to most preferred. Value are overwritten not merged:
      - /opt/grifter/
      - ~/.grifter/
      - ./
    :param guest_defaults_file: Guest defaults filename
    :return: Dict of guest default data or empty dict
    """
    guest_defaults = {}

    for directory in GUEST_DEFAULTS_DIRS:
        try:
            guest_defaults = load_data(f'{directory}/{guest_defaults_file}')
        except FileNotFoundError:
            logging.warning(f'File "{directory}/{guest_defaults_file}" not found')
        except PermissionError:
            logging.warning(f'File "{directory}/{guest_defaults_file}" permission denied')

    return guest_defaults


def update_guest_data(
        guest_data,
        guest_defaults_file='guest-defaults.yml',
        all_guest_defaults=ALL_GUEST_DEFAULTS):
    """
    Build data vars for guests. This function will take all_guest_defaults and merge in
    guest and guest group vars.
    :param guest_data: Dict of guest data
    :param guest_defaults_file: Guest defaults filename
    :param all_guest_defaults: All guest default data
    :return: Updated Dict of guest data
    """

    guest_defaults = load_guest_defaults(guest_defaults_file)

    new_guest_data = {'guests': []}
    for guest in guest_data['guests']:
        # Copy the default dict, that contains all top level variables
        # Group vars, then host vars will be merged into this dict
        default_context = copy.deepcopy(all_guest_defaults['guest_defaults'])
        if guest_defaults and guest['vagrant_box'].get('name') in guest_defaults:
            # Merge group vars with host vars
            group_context = guest_defaults.get(guest['vagrant_box']['name'])
            new_context = update_context(group_context, default_context)
            new_guest_data['guests'].append(update_context(guest, new_context))
        else:
            # No group vars found, just merge host vars
            new_guest_data['guests'].append(update_context(guest, default_context))
    return new_guest_data


def add_blackhole_interfaces(total_interfaces, interface_list):
    """
    Adds blackhole interfaces to host data by inserting a
    dict of blackhole config in the correct interface index position.
    :param total_interfaces: Total number of interfaces.
    :param interface_list: List of interface dicts to update.
    :return: New list of interface dicts.
    """
    if total_interfaces == len(interface_list):
        return interface_list

    updated_interface_list = []
    for i in range(1, total_interfaces + 1):
        blackhole_interface = {
            'name': f'bh-int{i}',
            'local_port': i,
            'remote_guest': 'blackhole',
            'remote_port': 666
        }
        try:
            for interface in interface_list:
                if interface['local_port'] == i:
                    updated_interface_list.append(interface)
                    # When a port number is matched terminate the
                    # loop to prevent adding unnecessary interfaces.
                    break
            else:
                # No match on the port number so add a blackhole interface.
                updated_interface_list.append(blackhole_interface)
        except IndexError:
            # Have run out of interfaces in the original list.
            # Blackhole interfaces will populate the rest of the list
            updated_interface_list.append(blackhole_interface)

    return updated_interface_list


def update_guest_interfaces(guest_data):
    """
    Entrypoint to updating guest data parameters.
    :param guest_data: List of host dicts.
    :return: New list of host dicts.
    """
    updated_guest_list = []
    for guest in guest_data:
        if not guest.get('interfaces'):
            updated_guest_list.append(guest)
        else:
            guest['interfaces'] = add_blackhole_interfaces(
                guest['provider_config']['nic_adapter_count'], guest['interfaces']
            )
            updated_guest_list.append(guest)

    return updated_guest_list


def validate_data(data):
    """
    Validate data conforms to required schema
    :param data: Guest data dict
    :return: errors dict
    """
    result = validate_schema(data, load_data(GUESTS_SCHEMA_FILE))
    errors = [result.errors] if result.errors else []

    for guest in data['guests']:
        result = validate_schema(guest, load_data(GUEST_SCHEMA_FILE))
        if result.errors:
            errors.append(result.errors)

    return errors


def generate_vagrant_file(
        data, loopbacks, template_name='guest.j2',
        template_directory=f'{TEMPLATES_DIR}/', vagrantfile_location='.'
        ):
    """
    Generate a vagrant file
    :param data: Dictionary of data to apply to Jinja2 template.
    :param loopbacks: Dictionary of loopback addresses.
    :param template_name: Name of Jinja2 template
    :param template_directory: Template directory location
    :param vagrantfile_location: location to save the Vagrantfile.
    :return: 
    """
    with open(f'{vagrantfile_location}/Vagrantfile', 'w') as f:
        vagrantfile = render_from_template(
            template_name=template_name,
            template_directory=template_directory,
            custom_filters=custom_filters,
            guests=data['guests'],
            loopbacks=loopbacks
        )

        f.write(vagrantfile)
