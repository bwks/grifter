from grifter.constants import ALL_GUEST_DEFAULTS

expected_all_guest_defaults = {
    'guest_defaults': {
        'name': '',
        'vagrant_box': {
            'name': '',
            'version': '',
            'provider': 'libvirt',
            'guest_type': '',
            'boot_timeout': 0
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
            'random_hostname': True,
            'nic_adapter_count': 0,
            'disk_bus': '',
            'cpus': 1,
            'memory': 512,
            'management_network_mac': '',
            'nic_model_type': '',
            'storage_pool': ''
        },
        'interfaces': []
    }
}


def test_default_values():
    assert expected_all_guest_defaults == ALL_GUEST_DEFAULTS
