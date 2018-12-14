import os
import copy
import logging
import random
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
    GUEST_DEFAULTS_DIRS,
    DEFAULT_CONFIG_FILE,
)

logger = logging.getLogger(__name__)

custom_filters = [
    explode_port,
]


def int_to_port_map(name, offset, number_of_interfaces):
    """
    Create a dict of interfaces to port maps
    :param name: Name of the base interface without the port number eg: swp
    :param offset: Number of the first interfaces eg: 0 or 1
    :param number_of_interfaces: Number of interfaces to create
    :return: Dictionary of interface to data port mappings
    """
    mapping = {}
    for i in range(offset, number_of_interfaces + offset):
        mapping.update({i: f'{name}{i}'})
    return mapping


def generate_int_to_port_mappings(dev):
    """
    Generate a dictionary of interface to port mappings
    :param dev: Dictionary with the following keys
                - data_interface_base
                - data_interface_offset
                - max_data_interfaces
                - internal_interfaces
                - reserved_interfaces
    :return: Dictionary of interface to port mappings
    """
    if dev['data_interface_base']:
        data_interfaces = int_to_port_map(dev['data_interface_base'],
                                          dev['data_interface_offset'],
                                          dev['max_data_interfaces'])
    else:
        data_interfaces = {}

    if dev['internal_interfaces']:
        internal_interfaces = int_to_port_map(
            'internal-', 1, dev['internal_interfaces'])
    else:
        internal_interfaces = {}

    if dev['reserved_interfaces']:
        reserved_interfaces = int_to_port_map(
            'reserved-', 1, dev['reserved_interfaces'])
    else:
        reserved_interfaces = {}

    return {
        'data_interfaces': data_interfaces,
        'internal_interfaces': internal_interfaces,
        'management_interface': dev['management_interface'],
        'reserved_interfaces': reserved_interfaces,
    }


def generate_guest_interface_mappings(config_file=DEFAULT_CONFIG_FILE):
    """
    Create a guest type to interfaces port map dictionary
    :param config_file: Path to config file
    :return: Dictionary of guest type interface port mappings.
    """
    config = load_data(config_file)
    mappings = {}
    for k, v in config['guest_config'].items():
        mappings[k] = generate_int_to_port_mappings(config['guest_config'][k])
    return mappings


def generate_loopbacks(guest_dict=None):
    """
    Generate a dict of loopback addresses
    :param guest_dict: List of guests
    :return: Dictionary of loopback addresses
    """
    if guest_dict is None or not isinstance(guest_dict, dict):
        raise AttributeError('guest_dict should contain a list of guests')
    elif not guest_dict:
        raise ValueError('dict of guests is empty')

    network = f'127.{random.randint(2, 254)}.{random.randint(2, 254)}'

    guests = list(guest_dict.keys())
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
            logger.info(f'File: "{directory}/{guest_defaults_file}" found')
        except FileNotFoundError:
            logger.warning(f'File: "{directory}/{guest_defaults_file}" not found')
        except PermissionError:
            logger.error(f'File: "{directory}/{guest_defaults_file}" permission denied')

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

    new_guest_data = {}
    for guest, data in guest_data.items():
        # Copy the default dict, that contains all top level variables
        # Group vars, then host vars will be merged into this dict
        default_context = copy.deepcopy(all_guest_defaults['guest_defaults'])
        if guest_defaults and data['vagrant_box'].get('name') in guest_defaults:
            # Merge group vars with host vars
            group_context = guest_defaults.get(data['vagrant_box']['name'])
            new_context = update_context(group_context, default_context)
            new_guest_data.update({guest: (update_context(data, new_context))})
        else:
            # No group vars found, just merge host vars
            new_guest_data.update({guest: (update_context(data, default_context))})
    return new_guest_data


def blackhole_interface_config(port_number):
    return {
        'local_port': port_number,
        'remote_guest': 'blackhole',
        'remote_port': 666
        }


def add_blackhole_interfaces(offset, total_interfaces, interface_list):
    """
    Adds blackhole interfaces to host data by inserting a
    dict of blackhole config in the correct interface index position.
    :param offset: Interface numbering offset.
    :param total_interfaces: Total number of interfaces.
    :param interface_list: List of interface dicts to update.
    :return: New list of interface dicts.
    """
    if total_interfaces == len(interface_list):
        return interface_list

    updated_interface_list = []
    for i in range(offset, total_interfaces + offset):
        for interface in interface_list:
            try:
                if interface['local_port'] == i:
                    updated_interface_list.append(interface)
                    # When a port number is matched terminate the
                    # loop to prevent adding unnecessary interfaces.
                    break
            except IndexError:
                # Have run out of interfaces in the original list.
                # Blackhole interfaces will populate the rest of the list
                updated_interface_list.append(blackhole_interface_config(i))
        else:
            # No match on the port number so add a blackhole interface.
            updated_interface_list.append(blackhole_interface_config(i))

    return updated_interface_list


def create_reserved_interfaces(num_reserved_interfaces):
    return [blackhole_interface_config(i) for i in range(1, num_reserved_interfaces + 1)]


def update_guest_interfaces(guest_data, config):
    """
    Entrypoint to updating guest data parameters.
    :param guest_data: List of host dicts.
    :return: New list of host dicts.
    """
    updated_guest_dict = {}
    for guest, data in guest_data.items():
        guest_box = data['vagrant_box']['name']
        if not data.get('data_interfaces'):
            updated_guest_dict.update({guest: data})
        else:
            data['data_interfaces'] = add_blackhole_interfaces(
                config['guest_config'][guest_box]['data_interface_offset'],
                data['provider_config']['nic_adapter_count'],
                data['data_interfaces']
            )
            updated_guest_dict.update({guest: data})

    return updated_guest_dict


def update_guest_additional_storage(guest_data):
    """
    Add storage volume size to additional storage volumes
    :param guest_data: List of host dicts.
    :return: New dict of guest data.
    """
    updated_guest_dict = {}
    for guest, data in guest_data.items():
        if not data['provider_config'].get('additional_storage_volumes'):
            updated_guest_dict.update({guest: data})
        else:
            for volume in data['provider_config']['additional_storage_volumes']:
                try:
                    volume['size'] = os.path.getsize(volume['location'])
                except OSError:
                    raise OSError(f'No such file: {volume["location"]}')
            updated_guest_dict.update({guest: data})

    return updated_guest_dict


def validate_data(guest_data):
    """
    Validate data conforms to required schema
    :param guest_data: Guest data dict
    :return: errors dict
    """
    errors = []
    for guest, data in guest_data.items():
        result = validate_schema(data, load_data(GUEST_SCHEMA_FILE))
        if result.errors:
            errors.append(result.errors)

    return errors


def generate_vagrant_file(
        guest_data, loopbacks, template_name='guest.j2',
        template_directory=f'{TEMPLATES_DIR}/', vagrantfile_location='.'
        ):
    """
    Generate a vagrant file
    :param guest_data: Dictionary of data to apply to Jinja2 template.
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
            guests=guest_data,
            loopbacks=loopbacks,
            interface_mappings=generate_guest_interface_mappings()
        )

        f.write(vagrantfile)
