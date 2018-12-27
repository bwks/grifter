import random
import uuid
import string
import re

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
    reduced = set()
    for i in list_of_tuples:
        if not (i[2], i[3], i[0], i[1]) in reduced:
            reduced.add(i)
    return list(reduced)


def sort_nicely(the_list):
    """
    Sort the given list in the way that humans expect.
    from: https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    :param the_list: The list to sort.
    """
    if the_list:
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        the_list.sort(key=alphanum_key)
