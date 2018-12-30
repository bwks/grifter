import os
import copy
import logging
import random
import pathlib
import time

from .utils import (
    get_uuid,
    remove_duplicates,
    sort_nicely,
    dict_merge,
)
from .custom_filters import (
    explode_port,
)
from .loaders import (
    render_from_template,
    load_data,
    load_config_file,
)
from .constants import (
    TEMPLATES_DIR,
    BLACKHOLE_LOOPBACK_MAP,
    ALL_GUEST_DEFAULTS,
    DEFAULT_CONFIG_FILE,
    VAGRANTFILE_BACKUP_DIR,
    TIMESTAMP_FORMAT,
)

logger = logging.getLogger(__name__)

custom_filters = [
    explode_port,
]


def get_default_config(config=DEFAULT_CONFIG_FILE):
    return load_data(config)


def generate_connection_strings(connections, dotfile=False):
    """
    Generate a list of connection strings. The format of connections
    is the output from the 'generate_int_to_port_mappings' function.
    :param connections: List of dicts containing connection information ie:
      [{'local_guest': 'p1sw1',
        'local_port': 'swp7',
        'remote_guest': 'p1r7',
        'remote_port': 'ge-0/0/9'}]
    :param dotfile: Generate a dotfile format undirected link
    :return: List of connection strings
    """
    def make_link(x):
        if dotfile:
            return f'''"{x['local_guest']}":"{x['local_port']}" -- "{x['remote_guest']}":"{x['remote_port']}";'''
        else:
            return f"{x['local_guest']}-{x['local_port']} <--> {x['remote_guest']}-{x['remote_port']}"
    connections_list = []
    for connection in connections:
        connections_list.append(make_link(connection))
    return sort_nicely(connections_list)


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


def generate_int_to_port_mappings(data):
    """
    Generate a dictionary of interface to port mappings
    :param data: Dictionary with the following keys
                - data_interface_base
                - data_interface_offset
                - max_data_interfaces
                - internal_interfaces
                - reserved_interfaces
    :return: Dictionary of interface to port mappings
    """
    if data.get('data_interface_base'):
        data_interfaces = int_to_port_map(data['data_interface_base'],
                                          data['data_interface_offset'],
                                          data['max_data_interfaces'])
    else:
        data_interfaces = {}

    if data.get('internal_interfaces'):
        internal_interfaces = int_to_port_map(
            'internal-', 1, data['internal_interfaces'])
    else:
        internal_interfaces = {}

    if data.get('reserved_interfaces'):
        reserved_interfaces = int_to_port_map(
            'reserved-', 1, data['reserved_interfaces'])
    else:
        reserved_interfaces = {}

    return {
        'data_interfaces': data_interfaces,
        'internal_interfaces': internal_interfaces,
        'management_interface': data.get('management_interface', 'mgmt'),
        'reserved_interfaces': reserved_interfaces,
    }


def generate_guest_interface_mappings(config_file=DEFAULT_CONFIG_FILE):
    """
    Create a guest type to interfaces port map dictionary
    :param config_file: Path to config file
    :return: Dictionary of guest type interface port mappings.
    """
    config = get_default_config(config_file)
    mappings = {}
    for k, v in config['guest_config'].items():
        mappings[k] = generate_int_to_port_mappings(config['guest_config'][k])
    return mappings


def generate_connections_list(guests, int_map, unique=False):
    """
    Generate a map of interface connections.
    :param guests: Dict of guests data
    :param int_map: Dict of interface mappings
    :param unique: Remove duplicate connection between guests
    :return: List of Dicts of connections between guests
    """
    dict_keys = ('local_guest', 'local_port', 'remote_guest', 'remote_port')
    connections = []
    box_map = {k: v['vagrant_box']['name'] for k, v in guests.items()}
    for k, v in guests.items():
        if v.get('data_interfaces'):
            for i in v['data_interfaces']:
                if not i['remote_guest'] == 'blackhole':
                    local_box = box_map[k]
                    local_int = int_map[local_box]['data_interfaces'][i['local_port']]
                    remote_box = box_map[i['remote_guest']]
                    remote_int = int_map[remote_box]['data_interfaces'][i['remote_port']]
                    connections.append((k, local_int, i['remote_guest'], remote_int))
    if unique:
        return [dict(zip(dict_keys, i)) for i in remove_duplicates(connections)]
    return [dict(zip(dict_keys, i)) for i in connections]


def create_reserved_interfaces(num_reserved_interfaces):
    return [blackhole_interface_config(i) for i in range(1, num_reserved_interfaces + 1)]


def generate_blackhole_interface_map(guests, int_map):
    blackhole_interfaces = {}
    for guest, data in guests.items():
        blackhole_interfaces.update({guest: []})
        guest_box = data['vagrant_box']['name']
        for interface in data['data_interfaces']:
            if interface['remote_guest'] == 'blackhole':
                blackhole_interfaces[guest].append(
                    int_map[guest_box]['data_interfaces'][interface['local_port']]
                )
    return blackhole_interfaces


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

    def generate_network():
        net = f'127.{random.randint(2, 254)}.{random.randint(2, 254)}'
        if net == '127.6.6':
            generate_network()
        return net
    network = generate_network()
    guests = list(guest_dict.keys())
    loopbacks = [f'{network}.{i}' for i in range(1, len(guests) + 1)]
    guest_to_loopback_map = dict(zip(guests, loopbacks))

    return {**guest_to_loopback_map, **BLACKHOLE_LOOPBACK_MAP}


def merge_user_config():
    default_config = get_default_config()
    user_config = load_config_file('config.yml')
    if user_config:
        merged_config = dict_merge(copy.deepcopy(default_config), user_config)
        return merged_config
    return default_config


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

    guest_defaults = load_config_file(guest_defaults_file)

    new_guest_data = {}
    for guest, data in guest_data.items():
        # Copy the default dict, that contains all top level variables
        # Group vars, then host vars will be merged into this dict
        default_context = copy.deepcopy(all_guest_defaults['guest_defaults'])
        if guest_defaults and data['vagrant_box'].get('name') in guest_defaults:
            # Merge group vars with host vars
            group_context = guest_defaults.get(data['vagrant_box']['name'])
            new_context = dict_merge(default_context, group_context)
            new_guest_data.update({guest: (dict_merge(new_context, data))})
        else:
            # No group vars found, just merge host vars
            new_guest_data.update({guest: (dict_merge(default_context, data))})
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


def update_reserved_interfaces(guest_data, config):
    updated_guest_dict = {}
    for guest, data in guest_data.items():
        guest_box = data['vagrant_box']['name']
        num_reserved_interfaces = config['guest_config'][guest_box]['reserved_interfaces']
        if not num_reserved_interfaces:
            updated_guest_dict.update({guest: data})
        else:
            data['reserved_interfaces'] = create_reserved_interfaces(num_reserved_interfaces)
            updated_guest_dict.update({guest: data})
    return updated_guest_dict


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
            updated_interfaces = add_blackhole_interfaces(
                config['guest_config'][guest_box]['data_interface_offset'],
                data['provider_config']['nic_adapter_count'],
                copy.deepcopy(data['data_interfaces'])
            )
            data['data_interfaces'] = updated_interfaces
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


def generate_vagrant_file(
        guest_data, loopbacks, template_name='guest.j2',
        template_directory=f'{TEMPLATES_DIR}/'
        ):
    """
    Generate a Vagrantfile in the current directory.
    :param guest_data: Dictionary of data to apply to Jinja2 template.
    :param loopbacks: Dictionary of loopback addresses.
    :param template_name: Name of Jinja2 template
    :param template_directory: Template directory location
    """
    time_now = time.strftime(TIMESTAMP_FORMAT)
    current_vagrantfile = pathlib.Path('Vagrantfile')
    if current_vagrantfile.exists():
        backup_dir = pathlib.Path(VAGRANTFILE_BACKUP_DIR)
        if not backup_dir.exists():
            backup_dir.mkdir()
        dest_file = pathlib.Path(f'{VAGRANTFILE_BACKUP_DIR}/Vagrantfile-{time_now}')
        src_file = pathlib.Path('Vagrantfile')
        src_file.replace(dest_file)

    interface_map = generate_guest_interface_mappings()
    blackhole_interface_map = generate_blackhole_interface_map(guest_data, interface_map)
    with open('Vagrantfile', 'w') as f:
        vagrantfile = render_from_template(
            template_name=template_name,
            template_directory=template_directory,
            custom_filters=custom_filters,
            guests=guest_data,
            loopbacks=loopbacks,
            interface_mappings=interface_map,
            domain_uuid=get_uuid(),
            creation_time=time_now,
            blackhole_interfaces=blackhole_interface_map,
        )
        f.write(vagrantfile)
        logger.info('Vagrantfile created')


def generate_dotfile(connections_list):
    """
    Generate undirected dotfile.
    :param connections_list: List of connections strings
    """
    with open('topology.dot', 'w') as f:
        dotfile = render_from_template(
            template_name='topology.dot.j2',
            template_directory=f'{TEMPLATES_DIR}/',
            connections_list=connections_list,
        )
        f.write(dotfile)
        logger.info('topology.dot file created')
