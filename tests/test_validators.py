import copy
import pytest

from .mock_data import mock_guest_data

from vagrantfile_builder.validators import (
    validate_required_keys,
    validate_required_values,
)


def mock_guest_remove_key(popme):
    guest = copy.deepcopy(mock_guest_data['guests'][0])
    return guest.pop(popme)


@pytest.mark.parametrize('value', [
    'name',
    'vagrant_box',
])
def test_validate_missing_required_key_name_raises_attribute_error(value):
    with pytest.raises(AttributeError):
        validate_required_keys(mock_guest_remove_key(value))


def test_validate_missing_required_key_vagrant_box_name_raises_attribute_error():
    guest = copy.deepcopy(mock_guest_data['guests'][0])
    guest['vagrant_box'].pop('name')
    with pytest.raises(AttributeError):
        validate_required_keys(mock_guest_remove_key('name'))


def test_validate_empty_required_name_raises_value_error():
    mock_guest_data['guests'][0]['name'] = ''
    with pytest.raises(ValueError):
        validate_required_values(mock_guest_data['guests'][0])


def test_validate_empty_required_vagrant_box_name_raises_value_error():
    mock_guest_data['guests'][0]['vagrant_box']['name'] = ''
    with pytest.raises(ValueError):
        validate_required_values(mock_guest_data['guests'][0])
