from vagrantfile_builder.constants import (
    BASE_DIR,
    ALL_GUEST_DEFAULTS,
)

from vagrantfile_builder.utils import (
    get_mac,
    update_context,
    create_guest_data,
)


def test_get_mac_returns_default_oui():
    assert get_mac()[0:8] == '28:b7:ad'


def test_get_mac_returns_custom_oui():
    assert get_mac('00:00:00')[0:8] == '00:00:00'


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
            'nic_adapter_count': 2
          },
          'synced_folder': {
            'enabled': False
          },
          'vagrant_box': {
            'boot_timeout': 0,
            'name': 'arista/veos',
            'provider': 'libvirt',
            'type': 'other',
            'version': '4.20.1F'
          }
        }
      ]
    }

    assert expected == create_guest_data(seed_data, f'{BASE_DIR}/../examples/guest-defaults.yml')


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
            'nic_adapter_count': 0
          },
          'synced_folder': {
            'enabled': False
          },
          'vagrant_box': {
            'boot_timeout': 0,
            'name': '',
            'provider': 'libvirt',
            'type': 'other',
            'version': ''
          }
        }
      ]
    }

    assert expected == create_guest_data(seed_data, 'does-not-exist.yml')
