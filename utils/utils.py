import random


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
    loopbacks = ['{0}.{1}'.format(network, i) for i in range(1, len(hosts) + 1)]

    return dict(zip(hosts, loopbacks))


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return '{0}:{1}'.format(oui, nic)
