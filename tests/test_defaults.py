from grifter.constants import ALL_GUEST_DEFAULTS

expected_guest_defaults = {
    'vagrant_box': {
        'name': '',
        'version': '',
        'url': '',
        'provider': 'libvirt',
        'guest_type': '',
        'boot_timeout': 0,
        'throttle_cpu': 0
    },
    'ssh': {
        'username': '',
        'password': '',
        'insert_key': False,
    },
    'synced_folder': {
        'enabled': False,
    },
    'provider_config': {
        'random_hostname': False,
        'nic_adapter_count': 0,
        'disk_bus': '',
        'cpus': 1,
        'memory': 512,
        'huge_pages': False,
        'management_network_mac': '',
        'nic_model_type': '',
        'storage_pool': '',
        'additional_storage_volumes': []
    },
    'data_interfaces': [],
    'internal_interfaces': [],
    'reserved_interfaces': []
}

expected_guest_config_defaults = {
    'data_interface_base': '',
    'data_interface_offset': 0,
    'internal_interfaces': 0,
    'max_data_interfaces': 8,
    'management_interface': 'mgmt',
    'reserved_interfaces': 0,
}


def test_default_values():
    assert expected_guest_defaults == ALL_GUEST_DEFAULTS['guest_defaults']


def test_config_default_values():
    assert expected_guest_config_defaults == ALL_GUEST_DEFAULTS['guest_config_defaults']
