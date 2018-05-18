import random
import copy

from .constants import ALL_GUEST_DEFAULTS
from .loaders import load_data


def get_mac(oui='28:b7:ad'):
    """
    Generate a random MAC address.
    param oui: MAC address OUI
    return: MAC address as a string
    """
    nic = ':'.join([format(random.randint(0, 255), '02x') for _ in range(0, 3)])
    return f'{oui}:{nic}'


def update_context(source, target):
    """
    Take a source dict and update it with target data
    :param source: Source data dictionary
    :param target: Target data dictionary to update
    :return: Return new dict with merged data
    """
    new_context = copy.deepcopy(target)
    for k, v in source.items():
        if k in target:
            if isinstance(target[k], dict):
                new_context[k].update(source[k])
            else:
                new_context[k] = source[k]

    return new_context


def create_guest_data(
        guest_data,
        guest_defaults='./guest-defaults.yml',
        all_guest_defaults=ALL_GUEST_DEFAULTS):
    """
    Build data vars for guests. This function will take all_guest_defaults and merge in
    guest and guest group vars.
    :param guest_data: Dict of guest data
    :param guest_defaults: Location of guest defaults file
    :param all_guest_defaults: All guest default data
    :return: Updated Dict of guest data
    """
    try:
        guest_defaults = load_data(guest_defaults)
    except FileNotFoundError:
        print('File: {} not found')
        guest_defaults = {}

    new_guest_data = {'guests': []}
    for guest in guest_data['guests']:
        # Copy the default dict, that contains all top level variables
        # Group vars, then host vars will be merged into this dict
        default_context = copy.deepcopy(all_guest_defaults['guest_defaults'])
        if guest_defaults and guest['vagrant_box'].get('name') in guest_defaults:
            # Merge group vars with host vars
            group_context = guest_defaults.get(guest['vagrant_box']['name'])
            new_context = update_context(group_context, default_context)
            new_guest_data['guests'].append(update_context(guest, new_context))
        else:
            # No group vars found, just merge host vars
            new_guest_data['guests'].append(update_context(guest, default_context))
    return new_guest_data
