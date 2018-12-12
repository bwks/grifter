import copy
import pytest

from unittest import mock

from grifter.constants import (
    BASE_DIR,
)

from grifter.loaders import (
    load_data,
)

from grifter.api import (
    generate_loopbacks,
    update_guest_interfaces,
    add_blackhole_interfaces,
    update_guest_data,
    update_context,
    validate_data,
    load_guest_defaults,
    update_guest_additional_storage,
    int_to_port_map,
    generate_int_to_port_mappings,
)

from .mock_data import (
    mock_guest_data,
    mock_guest_interfaces,
)


def mock_data(filename):
    return load_data(f'{filename}')


def test_guest_data_matches_dict():
    assert load_data('examples/guests.yml') == mock_guest_data


def test_generate_loopbacks_guest_list_not_list_type_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(guest_list="")


def test_generate_loopbacks_guest_list_is_none_raises_exception():
    with pytest.raises(AttributeError):
        generate_loopbacks(guest_list=None)


def test_generate_loopbacks_guest_list_empty_raises_exception():
    with pytest.raises(ValueError):
        generate_loopbacks(guest_list=[])


@mock.patch('random.randint', return_value=255)
def test_generate_loopbacks_returned_loopback_dict(mock_random):
    expected_loopback_dict = {
        'blackhole': '127.6.6.6',
        'sw01': '127.255.255.1',
        'sw02': '127.255.255.2'
    }
    assert generate_loopbacks(mock_guest_data['guests']) == expected_loopback_dict


def test_guest_without_interfaces():
    expected = {
        'guests': [
            {
                'ssh': {
                    'username': '',
                    'password': '',
                    'insert_key': False,
                },
                'name': 'sw01',
                'provider_config': {
                    'random_hostname': False,
                    'cpus': 2,
                    'disk_bus': 'ide',
                    'management_network_mac': '',
                    'nic_model_type': '',
                    'memory': 2048,
                    'huge_pages': False,
                    'nic_adapter_count': 2,
                    'additional_storage_volumes': []
                },
                'synced_folder': {
                    'enabled': False,
                },
                'vagrant_box': {
                    'name': 'arista/veos',
                    'provider': 'libvirt',
                    'version': '',
                    'url': '',
                    'guest_type': ''
                }
            },
            {
                'ssh': {
                    'username': '',
                    'password': '',
                    'insert_key': False,
                },
                'interfaces': [
                    {
                        'local_port': 1,
                        'name': 'eth1',
                        'remote_guest': 'sw01',
                        'remote_port': 1
                    },
                    {
                        'local_port': 2,
                        'name': 'eth2',
                        'remote_guest': 'sw01',
                        'remote_port': 2
                    }
                ],
                'name': 'sw02',
                'provider_config': {
                    'random_hostname': False,
                    'cpus': 2,
                    'disk_bus': 'ide',
                    'management_network_mac': '',
                    'nic_model_type': '',
                    'memory': 2048,
                    'huge_pages': False,
                    'nic_adapter_count': 2,
                    'additional_storage_volumes': []
                },
                'synced_folder': {
                    'enabled': False,
                },
                'vagrant_box': {
                    'name': 'arista/veos',
                    'provider': 'libvirt',
                    'version': '',
                    'url': '',
                    'guest_type': ''
                }
            }
        ]
    }

    guests = copy.deepcopy(mock_guest_data)
    guests['guests'][0].pop('interfaces')
    assert update_guest_interfaces(guests['guests']) == expected['guests']


def test_update_interfaces_with_same_interface_count_returns_same_list_of_interfaces():
    assert add_blackhole_interfaces(2, mock_guest_interfaces) == mock_guest_interfaces


def test_update_interfaces_with_blackhole_interfaces():
    blackhole_interfaces = [
        {
            'name': f'bh-int3',
            'local_port': 3,
            'remote_guest': 'blackhole',
            'remote_port': 666
        },
        {
            'name': f'bh-int4',
            'local_port': 4,
            'remote_guest': 'blackhole',
            'remote_port': 666
        }
    ]

    expected_intefaces = mock_guest_interfaces + blackhole_interfaces

    assert add_blackhole_interfaces(4, mock_guest_interfaces) == expected_intefaces


def test_update_context_with_dict():
    default_data = {'guest': {'name': ''}, 'insert_ssh_key': False}
    seed_data = {'guest': {'name': 'sw01'}}

    expected = {'guest': {'name': 'sw01'}, 'insert_ssh_key': False}

    assert expected == update_context(seed_data, default_data)


def test_update_context_with_non_dict():
    default_data = {'guest': {'name': ''}, 'insert_ssh_key': False}
    seed_data = {'guest': {'name': 'sw01'}, 'insert_ssh_key': True}

    expected = {'guest': {'name': 'sw01'}, 'insert_ssh_key': True}

    assert expected == update_context(seed_data, default_data)


@mock.patch('grifter.api.load_guest_defaults', side_effect=mock_data)
def test_create_guest_with_group_vars(mock_data):
    seed_data = {'guests': [{'name': 'sw01', 'vagrant_box': {'name': 'arista/veos'}}]}

    expected = {
        'guests': [
            {
                'ssh': {
                    'username': '',
                    'password': '',
                    'insert_key': False,
                },
                'interfaces': [],
                'name': 'sw01',
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
                    'additional_storage_volumes': []
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
                    'url': ''
                }
            }
        ]
    }

    assert expected == update_guest_data(seed_data, f'{BASE_DIR}/../examples/guest-defaults.yml')


def test_create_guest_without_group_vars():
    seed_data = {'guests': [{'name': 'sw01'}]}

    expected = {
        'guests': [
            {
                'ssh': {
                    'username': '',
                    'password': '',
                    'insert_key': False,
                },
                'interfaces': [],
                'name': 'sw01',
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
                    'additional_storage_volumes': []
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
                    'url': ''
                }
            }
        ]
    }

    assert expected == update_guest_data(seed_data, 'does-not-exist.yml')


def test_validate_data_returns_list():
    result = validate_data({'guests': {}})
    assert isinstance(result, list)


def test_validate_data_with_valid_data_returns_no_errors_in_empty_list():
    result = validate_data(mock_guest_data)
    assert not result


def test_validate_data_with_invalid_data_returns_list_of_errors():
    # missing name field value
    data = {'guests': [{'name': '', 'vagrant_box': {'name': 'box-name'}}]}
    result = validate_data(data)
    assert result


@mock.patch('grifter.api.load_guest_defaults', side_effect=mock_data)
def test_load_guest_defaults_with_file_error_returns_empty_dict(mock_data):
    expected = {}
    assert expected == load_guest_defaults('blah.yml')


# noinspection PyPep8Naming
def test_update_guest_additional_storage_raises_OSError():
    guests = {
        'guests': [
            {
                'name': 'some_guest',
                'provider_config': {
                    'additional_storage_volumes': [
                        {'location': '/fake/path/file.img'}
                    ]
                }
            }
        ]
    }
    with pytest.raises(OSError):
        update_guest_additional_storage(guests['guests'])


@mock.patch('os.path.getsize', return_value='10000')
def test_update_guest_additional_storage_size(mock_data):
    guests = {
        'guests': [
            {
                'name': 'some_guest',
                'provider_config': {
                    'additional_storage_volumes': [
                        {'location': '/fake/path/file.img'}
                    ]
                }
            }
        ]
    }

    result = update_guest_additional_storage(guests['guests'])
    assert result[0]['provider_config']['additional_storage_volumes'][0]['size'] == '10000'


def test_int_to_port_map_returns_expected():
    expected = {f'ge-0/0/{i}': 10000 + i for i in range(0, 12)}
    result = int_to_port_map('ge-0/0/', 0, 12, 10000)
    assert result == expected


def test_generate_int_to_port_mappings():
    expected = {
        'data_interfaces': {f'ge-0/0/{i}': 10000 + i for i in range(0, 12)},
        'internal_interfaces': {'internal-1': 11001},
        'management_interface': 'fxp0.0',
        'reserved_interfaces': {'reserved-1': 12001}
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
