import copy
import pytest

from .mock_data import mock_guest_data

from grifter.constants import GUEST_SCHEMA_FILE

from grifter.loaders import load_data

from grifter.validators import (
    validate_required_keys,
    validate_required_values,
    validate_schema,
)


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
        validate_required_keys(guest)


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
