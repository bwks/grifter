import random

from constants import BLACKHOLE_LOOPBACK_MAP


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return f'{oui}:{nic}'


def generate_loopbacks(host_dict=None, network='127.255.1'):
    """
    Generate a dict of loopback addresses
    :param host_dict: List of hosts
    :param network: Network portion of the loopback addresses
    :return: List of loopback addresses
    """
    if host_dict is None or not isinstance(host_dict, dict):
        raise AttributeError('host_dict should contain a dict of hosts')
    elif not host_dict:
        raise ValueError('dict of hosts is empty')

    hosts = [i['name'] for i in host_dict['hosts']]
    loopbacks = [f'{network}.{i}' for i in range(1, len(hosts) + 1)]
    host_to_loopback_map = dict(zip(hosts, loopbacks))

    return {**host_to_loopback_map, **BLACKHOLE_LOOPBACK_MAP}


def update_interfaces(total_interfaces, interface_list):
    if total_interfaces == len(interface_list):
        return interface_list

    updated_interface_list = []
    for i in range(1, total_interfaces + 1):
        blackhole_interface = {
            'name': 'blackhole',
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
    updated_host_list = []
    for host in hosts:
        host['interfaces'] = update_interfaces(
            host['provider_config']['nic_adapter_count'], host['interfaces']
        )
        updated_host_list.append(host)

    return updated_host_list
