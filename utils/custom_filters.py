import random


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for i in range(0, 3)])
    return '{0}:{1}'.format(oui, nic)


def explode_port(port):
    """
    Create a high port number > 10000 for use with UDP tunnels
    :param port: port number to add to 10000
    :return: Int port number
    """
    if not isinstance(port, int) or port < 0 or port > 99:
        raise AttributeError('port must be and integer between 0 and 99')

    return 10000 + port
