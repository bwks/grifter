import copy
import pytest

from .mock_data import mock_guest_data

from grifter.api import (
    generate_guest_interface_mappings,
    get_default_config
)
from grifter.constants import (
    GUEST_SCHEMA_FILE,
    DEFAULT_CONFIG_FILE,
)

from grifter.loaders import load_data

from grifter.validators import (
    validate_required_keys,
    validate_required_values,
    validate_schema,
    validate_guests_in_guest_config,
    validate_guest_interfaces,
    validate_data,
    validate_config,
)

config = load_data(DEFAULT_CONFIG_FILE)
interface_mappings = generate_guest_interface_mappings()


def guest_data():
    return copy.deepcopy(mock_guest_data)


def mock_guest_remove_key(popme):
    guest = copy.deepcopy(mock_guest_data['sw01'])
    return guest.pop(popme)


@pytest.mark.parametrize('value', [
    'vagrant_box',
])
def test_validate_missing_required_key_name_raises_attribute_error(value):
    with pytest.raises(AttributeError):
        validate_required_keys(mock_guest_remove_key(value))


def test_validate_missing_required_key_vagrant_box_name_raises_attribute_error():
    guest = guest_data()
    guest['sw01']['vagrant_box'].pop('name')
    with pytest.raises(AttributeError):
        validate_required_keys(guest['sw01'])


def test_validate_empty_required_vagrant_box_name_raises_value_error():
    guest = guest_data()
    guest['sw01']['vagrant_box']['name'] = ''
    with pytest.raises(ValueError):
        validate_required_values(guest['sw01'])


def test_validate_schema():
    data = {'blah': ''}
    schema = {'blah': {'type': 'string'}}
    result = validate_schema(data, schema)
    assert not result.errors


def test_validate_guest_schema():
    data = {'vagrant_box': {'name': 'box-name'}}
    schema = load_data(GUEST_SCHEMA_FILE)
    result = validate_schema(data, schema)
    assert not result.errors


def test_validate_guests_in_guest_config_with_valid_config_returns_true():
    assert validate_guests_in_guest_config(mock_guest_data, config) is True


def test_validate_guests_in_guest_config_with_box_not_in_config_raises_attribute_error():
    data = guest_data()
    data['sw01']['vagrant_box']['name'] = 'blah/blah'
    with pytest.raises(AttributeError):
        validate_guests_in_guest_config(data, config)


def test_validate_guests_in_guest_config_with_missing_remote_guest_raises_attribute_error():
    data = guest_data()
    data['sw01']['data_interfaces'][0]['remote_guest'] = 'blah'
    with pytest.raises(AttributeError):
        validate_guests_in_guest_config(data, config)


def test_validate_guest_interfaces_more_data_interfaces_than_max_raises_attribute_error():
    data = guest_data()
    data['sw01']['provider_config']['nic_adapter_count'] = 100
    with pytest.raises(AttributeError):
        validate_guest_interfaces(data, config, interface_mappings)


def test_validate_guest_interfaces_local_port_outside_range_raises_attribute_error():
    data = guest_data()
    data['sw01']['data_interfaces'][0]['local_port'] = 100
    with pytest.raises(AttributeError):
        validate_guest_interfaces(data, config, interface_mappings)


def test_validate_guest_interfaces_remote_port_outside_range_raises_attribute_error():
    data = guest_data()
    data['sw01']['data_interfaces'][0]['remote_port'] = 100
    with pytest.raises(AttributeError):
        validate_guest_interfaces(data, config, interface_mappings)


def test_number_of_internal_interfaces():
    data = guest_data()
    data['sw01']['internal_interfaces'] = [1, 2]
    with pytest.raises(AttributeError):
        validate_guest_interfaces(data, config, interface_mappings)


def test_validate_guest_interfaces_with_valid_data_returns_true():
    data = guest_data()
    result = validate_guest_interfaces(data, config, interface_mappings)
    assert result is True


def test_validate_data_returns_list():
    result = validate_data({'guests': {}})
    assert isinstance(result, list)


def test_validate_data_with_valid_data_returns_no_errors_in_empty_list():
    result = validate_data(mock_guest_data)
    assert not result


def test_validate_data_with_invalid_data_returns_list_of_errors():
    # missing vagrant box name field value
    data = {'sw01': {'vagrant_box': {'name': ''}}}
    result = validate_data(data)
    assert result


def test_validate_config_default_config_returns_no_errors():
    default_config = get_default_config()
    result = validate_config(default_config)
    assert not result
