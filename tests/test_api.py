import copy
import pytest


from vagrantfile_builder.constants import (
    BASE_DIR,
)

from vagrantfile_builder.loaders import (
    load_data,
)

from vagrantfile_builder.api import (
    generate_loopbacks,
    update_guest_interfaces,
    add_blackhole_interfaces,
    update_guest_data,
    update_context,
    validate_data,
)

from .mock_data import (
    mock_guest_data,
    mock_guest_interfaces,
)


def test_host_data_matches_dict():
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


def test_generate_loopbacks_returned_loopback_dict():
    expected_loopback_dict = {
        'blackhole': '127.6.6.6',
        'sw01': '127.255.1.1',
        'sw02': '127.255.1.2'
    }
    assert generate_loopbacks(mock_guest_data['guests']) == expected_loopback_dict


def test_guest_without_interfaces():
    expected = {
        'guests': [
            {
                'insert_ssh_key': False,
                'name': 'sw01',
                'provider_config': {
                    'cpus': 2,
                    'disk_bus': 'ide',
                    'management_network_mac': '',
                    'memory': 2048,
                    'nic_adapter_count': 2
                },
                'synced_folder': {
                    'enabled': False,
                },
                'vagrant_box': {
                    'name': 'arista/veos',
                    'provider': 'libvirt',
                    'version': '',
                    'guest_type': ''
                }
            },
            {
                'insert_ssh_key': False,
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
                    'cpus': 2,
                    'disk_bus': 'ide',
                    'management_network_mac': '',
                    'memory': 2048,
                    'nic_adapter_count': 2
                },
                'synced_folder': {
                    'enabled': False,
                },
                'vagrant_box': {
                    'name': 'arista/veos',
                    'provider': 'libvirt',
                    'version': '',
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


def test_create_guest_with_group_vars():
    seed_data = {'guests': [{'name': 'sw01', 'vagrant_box': {'name': 'arista/veos'}}]}

    expected = {
      'guests': [
        {
          'insert_ssh_key': False,
          'interfaces': [],
          'name': 'sw01',
          'provider_config': {
            'cpus': 2,
            'disk_bus': 'ide',
            'management_network_mac': '',
            'memory': 2048,
            'nic_adapter_count': 8,
            'storage_pool': ''
          },
          'synced_folder': {
            'enabled': False
          },
          'vagrant_box': {
            'boot_timeout': 0,
            'name': 'arista/veos',
            'provider': 'libvirt',
            'guest_type': '',
            'version': '4.20.1F'
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
          'insert_ssh_key': False,
          'interfaces': [],
          'name': 'sw01',
          'provider_config': {
            'cpus': 1,
            'disk_bus': 'virtio',
            'management_network_mac': '',
            'memory': 512,
            'nic_adapter_count': 0,
            'storage_pool': ''
          },
          'synced_folder': {
            'enabled': False
          },
          'vagrant_box': {
            'boot_timeout': 0,
            'name': '',
            'provider': 'libvirt',
            'guest_type': '',
            'version': ''
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
