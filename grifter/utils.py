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


def remove_duplicates(list_of_tuples):
    """
    Takes a list of tuples and removes duplicate entries.
    Reverses the pairs (0, 1, 2, 3) to (2, 3, 0, 1) for comparison.
    :param list_of_tuples: [(0, 1, 2, 3), (2, 3, 0, 1)]
    :return: List of unique tuples.
    """
    reduced = []
    for i in list_of_tuples:
        if not (i[2], i[3], i[0], i[1]) in reduced:
            reduced.append(i)
    return reduced
