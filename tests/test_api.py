import copy
import pytest

from unittest import mock

from grifter.constants import (
    BASE_DIR,
    DEFAULT_CONFIG_FILE,
)
from grifter.loaders import (
    load_data,
    load_config_file,
)
from grifter.api import (
    generate_loopbacks,
    update_guest_interfaces,
    add_blackhole_interfaces,
    update_guest_data,
    update_guest_additional_storage,
    int_to_port_map,
    generate_int_to_port_mappings,
    create_reserved_interfaces,
    generate_connection_strings,
)
from .mock_data import (
    mock_guest_data,
    mock_guest_interfaces,
    mock_connection_data,
)

config = load_data(DEFAULT_CONFIG_FILE)


def mock_data(filename):
    return load_data(f'{filename}')


def test_guest_data_matches_dict():
    assert load_data('examples/guests.yml') == mock_guest_data


def test_generate_loopbacks_guest_dict_not_dict_type_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(guest_dict="")


def test_generate_loopbacks_guest_dict_is_none_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(guest_dict=None)


def test_generate_loopbacks_guest_dict_empty_raises_exception():
    with pytest.raises(ValueError):
        generate_loopbacks(guest_dict={})


@mock.patch('random.randint', return_value=255)
def test_generate_loopbacks_returned_loopback_dict(mock_random):
    expected_loopback_dict = {
        'blackhole': '127.6.6.6',
        'sw01': '127.255.255.1',
        'sw02': '127.255.255.2'
    }
    assert generate_loopbacks(mock_guest_data) == expected_loopback_dict


def test_guest_without_interfaces():
    expected = {
        'sw01': {
            'ssh': {
                'username': '',
                'password': '',
                'insert_key': False,
            },
            'internal_interfaces': [],
            'reserved_interfaces': [],
            'provider_config': {
                'random_hostname': False,
                'cpus': 2,
                'disk_bus': 'ide',
                'management_network_mac': '',
                'nic_model_type': '',
                'memory': 2048,
                'huge_pages': False,
                'nic_adapter_count': 2,
                'additional_storage_volumes': [],
            },
            'synced_folder': {
                'enabled': False,
            },
            'vagrant_box': {
                'name': 'arista/veos',
                'provider': 'libvirt',
                'version': '',
                'url': '',
                'guest_type': '',
                'throttle_cpu': 0
            }
        }
    }

    guests = copy.deepcopy(mock_guest_data)
    guests.pop('sw02')
    guests['sw01'].pop('data_interfaces')
    result = update_guest_interfaces(guests, config)
    assert result == expected


def test_update_interfaces_with_same_interface_count_returns_same_list_of_interfaces():
    assert add_blackhole_interfaces(1, 2, mock_guest_interfaces) == mock_guest_interfaces


def test_update_interfaces_with_blackhole_interfaces():
    blackhole_interfaces = [
        {
            'local_port': 3,
            'remote_guest': 'blackhole',
            'remote_port': 666
        },
        {
            'local_port': 4,
            'remote_guest': 'blackhole',
            'remote_port': 666
        }
    ]

    expected_intefaces = mock_guest_interfaces + blackhole_interfaces

    assert add_blackhole_interfaces(1, 4, mock_guest_interfaces) == expected_intefaces


@mock.patch('grifter.api.load_config_file', side_effect=mock_data)
def test_create_guest_with_group_vars(mock_data):
    seed_data = {'sw01': {'vagrant_box': {'name': 'arista/veos'}}}

    expected = {
        'sw01': {
            'ssh': {
                'username': '',
                'password': '',
                'insert_key': False,
            },
            'data_interfaces': [],
            'internal_interfaces': [],
            'reserved_interfaces': [],
            'provider_config': {
                'random_hostname': False,
                'cpus': 2,
                'disk_bus': 'ide',
                'management_network_mac': '',
                'nic_model_type': '',
                'memory': 2048,
                'huge_pages': False,
                'nic_adapter_count': 8,
                'storage_pool': '',
                'additional_storage_volumes': [],
            },
            'synced_folder': {
                'enabled': False
            },
            'vagrant_box': {
                'boot_timeout': 0,
                'name': 'arista/veos',
                'provider': 'libvirt',
                'guest_type': '',
                'version': '4.20.1F',
                'url': '',
                'throttle_cpu': 0
            }
        }
    }

    assert expected == update_guest_data(seed_data, f'{BASE_DIR}/../examples/guest-defaults.yml')


def test_create_guest_without_group_vars():
    seed_data = {'sw01': {}}

    expected = {
        'sw01': {
            'ssh': {
                'username': '',
                'password': '',
                'insert_key': False,
            },
            'data_interfaces': [],
            'internal_interfaces': [],
            'reserved_interfaces': [],
            'provider_config': {
                'random_hostname': False,
                'cpus': 1,
                'disk_bus': '',
                'management_network_mac': '',
                'nic_model_type': '',
                'memory': 512,
                'huge_pages': False,
                'nic_adapter_count': 0,
                'storage_pool': '',
                'additional_storage_volumes': [],
            },
            'synced_folder': {
                'enabled': False
            },
            'vagrant_box': {
                'boot_timeout': 0,
                'name': '',
                'provider': 'libvirt',
                'guest_type': '',
                'version': '',
                'url': '',
                'throttle_cpu': 0
            }
        }
    }

    assert expected == update_guest_data(seed_data, 'does-not-exist.yml')


@mock.patch('grifter.api.load_config_file', side_effect=mock_data)
def test_load_config_file_with_file_error_returns_empty_dict(mock_data):
    expected = {}
    assert expected == load_config_file('blah.yml')


# noinspection PyPep8Naming
def test_update_guest_additional_storage_raises_OSError():
    guests = {
        'some-guest': {
            'provider_config': {
                'additional_storage_volumes': [
                    {'location': '/fake/path/file.img'}
                ]
            }
        }
    }
    with pytest.raises(OSError):
        update_guest_additional_storage(guests)


@mock.patch('os.path.getsize', return_value='10000')
def test_update_guest_additional_storage_size(mock_data):
    guests = {
        'some-guest': {
            'provider_config': {
                'additional_storage_volumes': [
                    {'location': '/fake/path/file.img'}
                ]
            }
        }
    }
    result = update_guest_additional_storage(guests)
    assert result['some-guest']['provider_config']['additional_storage_volumes'][0]['size'] == '10000'


def test_int_to_port_map_returns_expected():
    expected = {}
    for i in range(0, 12):
        expected.update({0 + i: f'ge-0/0/{i}'})
    result = int_to_port_map('ge-0/0/', 0, 12)
    assert result == expected


def test_generate_int_to_port_mappings():
    data_interfaces = {}
    for i in range(0, 12):
        data_interfaces.update({0 + i: f'ge-0/0/{i}'})
    expected = {
        'data_interfaces': data_interfaces,
        'internal_interfaces': {1: 'internal-1'},
        'management_interface': 'fxp0.0',
        'reserved_interfaces': {1: 'reserved-1'}
    }
    data = {
        'data_interface_base': "ge-0/0/",
        'data_interface_offset': 0,
        'internal_interfaces': 1,
        'max_data_interfaces': 12,
        'management_interface': "fxp0.0",
        'reserved_interfaces': 1,
    }

    result = generate_int_to_port_mappings(data)
    assert result == expected


def test_generate_int_to_port_mappings_empty_interfaces_returns_empty_dict():
    expected = {
        'data_interfaces': {},
        'internal_interfaces': {},
        'management_interface': 'mgmt',
        'reserved_interfaces': {}
    }
    assert generate_int_to_port_mappings({}) == expected


def test_create_reserved_interfaces():
    expected = [{
        'local_port': 1,
        'remote_guest': 'blackhole',
        'remote_port': 666
    }]
    assert create_reserved_interfaces(1) == expected


@pytest.mark.parametrize('data ,expected, dotfile', [
    (mock_connection_data, ['sw1-swp7 <--> r7-ge-0/0/9'], False),
    (mock_connection_data, ['"sw1":"swp7" -- "r7":"ge-0/0/9";'], True),

])
def test_generate_connection_strings_return_expected_string_list(data, expected, dotfile):
    assert generate_connection_strings(data, dotfile) == expected
