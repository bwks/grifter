from cerberus import Validator
from grifter.loaders import load_data
from grifter.constants import (
    GUEST_SCHEMA_FILE,
    GUEST_CONFIG_SCHEMA,
    GUEST_PAIRS_SCHEMA,

)
required_keys = ['vagrant_box']


def validate_config(guest_config):
    errors = []

    def _validate(config, schema):
        validation_errors = []
        for key, data in config.items():
            result = validate_schema(data, schema)
            if result.errors:
                validation_errors.append(result.errors)
        return validation_errors

    guest_config_result = _validate(guest_config['guest_config'], load_data(GUEST_CONFIG_SCHEMA))
    guest_pairs_result = _validate(guest_config['guest_pairs'], load_data(GUEST_PAIRS_SCHEMA))

    if guest_config_result:
        errors += guest_config_result

    if guest_pairs_result:
        errors += guest_pairs_result

    return errors


def validate_data(guest_data, guest_default_data=False):
    """
    Validate data conforms to required schema
    :param guest_data: Guest data dict
    :param guest_default_data: True if validating guest defaults
    :return: errors list
    """
    errors = []
    schema = load_data(GUEST_SCHEMA_FILE)
    # Guest default schema should be the same as a guest
    # schema apart from the vagrant box name attribute.
    if guest_default_data:
        schema['vagrant_box']['schema'].pop('name')

    for guest, data in guest_data.items():
        result = validate_schema(data, schema)
        if result.errors:
            errors.append(result.errors)

    return errors


def validate_guests_in_guest_config(guests, config):
    """
    Validate guests have a vagrant box config
    :param guests:
    :param config:
    :return:
    """
    guest_config = config['guest_config']
    for guest, data in guests.items():
        local_guest = guest
        local_box = data['vagrant_box']['name']
        remote_guests = list(
            set([i['remote_guest'] for i in data['data_interfaces'] if i['remote_guest'] != 'blackhole'])
        )

        if not guest_config.get(local_box):
            raise AttributeError(
                f'{local_guest}\'s vagrant box type: {local_box} '
                f'is not defined in the config file.')

        for remote_guest in remote_guests:
            if not guests.get(remote_guest):
                raise AttributeError(
                    f'{remote_guest} is not defined in the guests file.')

    return True


def validate_guest_interfaces(guests, config, int_map):
    guest_config = config['guest_config']
    for guest, data in guests.items():
        local_guest = guest
        local_box = data['vagrant_box']['name']
        nic_adapter_count = data['provider_config']['nic_adapter_count']
        max_data_interfaces = guest_config[local_box]['max_data_interfaces']
        internal_interfaces = data['internal_interfaces']
        reserved_interfaces = data['reserved_interfaces']
        box_internal_interfaces = guest_config[local_box]['internal_interfaces']
        num_internal_interfaces = len(internal_interfaces)
        num_reserved_interfaces = len(reserved_interfaces)
        total_interfaces = max_data_interfaces + num_internal_interfaces + num_reserved_interfaces

        remote_guest_data = []
        if data['data_interfaces']:
            for i in data['data_interfaces']:
                if i['remote_guest'] != 'blackhole':
                    remote_guest_data.append((i['remote_guest'], i['remote_port']))

        if nic_adapter_count > total_interfaces:
            raise AttributeError(
                f'The number of data interfaces for {local_guest} '
                f'is greater than the allowed {local_box} maximum data interfaces.')

        for interface in data['data_interfaces']:
            local_port = interface["local_port"]
            if not int_map[local_box]['data_interfaces'].get(local_port):
                raise AttributeError(
                    f'{local_guest}\'s local_port: {local_port} '
                    f'is outside the supported range.')

        for rg in remote_guest_data:
            remote_guest = rg[0]
            remote_port = rg[1]
            remote_box = guests[remote_guest]['vagrant_box']['name']
            if not int_map[remote_box]['data_interfaces'].get(remote_port):
                raise AttributeError(
                    f'Error with {local_guest}\'s interface config.\n'
                    f'{remote_guest}\'s interface: {remote_port} '
                    f'is outside the supported range.')

        if num_internal_interfaces != box_internal_interfaces:
            raise AttributeError(
                f'The number of internal interfaces for {local_guest}: {num_internal_interfaces} '
                f'is not equal to the {local_box} internal interfaces value: '
                f'{box_internal_interfaces}.')
    return True


def validate_required_keys(guest):
    for key in required_keys:
        if not guest.get(key):
            raise AttributeError(f'{key} is a required key')
    if not guest['vagrant_box'].get('name'):
        raise AttributeError('vagrant_box["name"] is a required key')


def validate_required_values(guest):
    if not guest['vagrant_box']['name']:
        raise ValueError('vagrant_box["name"] is a required value and cannot be empty')


def validate_schema(data, schema):
    v = Validator()
    v.validate(data, schema)
    return v
