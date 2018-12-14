import random


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return f'{oui}:{nic}'


def sort_dict_by_value(data):
    # https://stackoverflow.com/a/34103440/2520425
    return dict(sorted(data.items(), key=lambda x: x[1]))
