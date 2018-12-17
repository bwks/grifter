import random
import uuid
import string


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return f'{oui}:{nic}'


def get_uuid():
    """
    Generate a random UUID.
    :return: random UUID string.
    """
    return str(uuid.uuid5(uuid.uuid4(), string.ascii_letters))
