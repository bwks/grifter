import random

from .defaults import defaults
from .loaders import render_from_template


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return f'{oui}:{nic}'


def create_host_data(data):
    """
    Build a base data file for host.
    :return:
    """
    pass
