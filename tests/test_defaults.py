from vagrantfile_builder.constants import ALL_GUEST_DEFAULTS

expected_all_guest_defaults = {
    'guest_defaults': {
        'name': '',
        'vagrant_box': {
            'name': '',
            'version': '',
            'provider': 'libvirt',
            'type': '',
            'boot_timeout': 0
        },
        'insert_ssh_key': False,
        'synced_folder': {
            'enabled': False,
        },
        'provider_config': {
            'nic_adapter_count': 0,
            'disk_bus': 'virtio',
            'cpus': 1,
            'memory': 512,
            'management_network_mac': '',
            'storage_pool': ''
        },
        'interfaces': []
    }
}


def test_default_values():
    assert expected_all_guest_defaults == ALL_GUEST_DEFAULTS
