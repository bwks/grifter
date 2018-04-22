import yaml

from .custom_filters import (
    explode_port,
)

from .loaders import (
    render_from_template,
)

from .constants import (
    TEMPLATE_DIR,
    BLACKHOLE_LOOPBACK_MAP,
)

custom_filters = [
    explode_port,
]


def load_host_data(location):
    """
    Load yaml file from location
    :param location: Location of YAML file
    :return: Dictionary of data
    """
    with open(location, 'r') as f:
        return yaml.load(f)


def generate_loopbacks(host_list=None, network='127.255.1'):
    """
    Generate a dict of loopback addresses
    :param host_list: List of hosts
    :param network: Network portion of the loopback addresses
    :return: Dictionary of loopback addresses
    """
    if host_list is None or not isinstance(host_list, list):
        raise AttributeError('host_list should contain a list of hosts')
    elif not host_list:
        raise ValueError('dict of hosts is empty')

    hosts = [i['name'] for i in host_list]
    loopbacks = [f'{network}.{i}' for i in range(1, len(hosts) + 1)]
    host_to_loopback_map = dict(zip(hosts, loopbacks))

    return {**host_to_loopback_map, **BLACKHOLE_LOOPBACK_MAP}


def update_interfaces(host_name, total_interfaces, interface_list):
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
            'name': f'{host_name}-bh-int{i}',
            'local_port': i,
            'remote_host': 'blackhole',
            'remote_port': 666
        }
        try:
            for interface in interface_list:
                if interface['local_port'] == i:
                    updated_interface_list.append(interface)
                    break
            else:
                updated_interface_list.append(blackhole_interface)
        except IndexError:
            updated_interface_list.append(blackhole_interface)

    return updated_interface_list


def update_hosts(hosts):
    """
    Entrypoint to updating host data parameters.
    :param hosts: List of host dicts.
    :return: New list of host dicts.
    """
    updated_host_list = []
    for host in hosts:
        host['interfaces'] = update_interfaces(
            host['name'], host['provider_config']['nic_adapter_count'], host['interfaces']
        )
        updated_host_list.append(host)

    return updated_host_list


def generate_vagrant_file(
        data, loopbacks, template_name='host.j2',
        template_directory=f'{TEMPLATE_DIR}/', vagrantfile_location='.'
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
            hosts=data['hosts'],
            loopbacks=loopbacks
        )

        f.write(vagrantfile)
