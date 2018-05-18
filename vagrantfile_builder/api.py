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
        raise ValueError('list of hosts is empty')

    hosts = [i['name'] for i in host_list]
    loopbacks = [f'{network}.{i}' for i in range(1, len(hosts) + 1)]
    host_to_loopback_map = dict(zip(hosts, loopbacks))

    return {**host_to_loopback_map, **BLACKHOLE_LOOPBACK_MAP}


def update_interfaces(total_interfaces, interface_list):
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
            'remote_host': 'blackhole',
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


def update_guests(guests):
    """
    Entrypoint to updating guest data parameters.
    :param guests: List of host dicts.
    :return: New list of host dicts.
    """
    updated_guest_list = []
    for guest in guests:
        if not guest.get('interfaces'):
            updated_guest_list.append(guest)
        else:
            guest['interfaces'] = update_interfaces(
                guest['provider_config']['nic_adapter_count'], guest['interfaces']
            )
            updated_guest_list.append(guest)

    return updated_guest_list


def generate_vagrant_file(
        data, loopbacks, template_name='guest.j2',
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
