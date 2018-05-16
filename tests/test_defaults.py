from vagrantfile_builder.defaults import defaults

all_defaults = {
    'guest_defaults': {
        'name': '',
        'vagrant_box': {
            'name': '',
            'version': '',
            'provider': 'libvirt',
            'guest_type': 'other',
            'boot_timeout': 0
        },
        'insert_ssh_key': False,
        'synced_folder': {
            'enabled': False,
            'id': 'vagrant-root',
            'src': '.',
            'dst': '/vagrant'
        },
        'provider_config': {
            'nic_adapter_count': 0,
            'disk_bus': 'virtio',
            'cpus': 1,
            'memory': 512,
            'management_network_mac': ''
        },
        'interfaces': []
    }
}


def test_default_values():
    assert all_defaults == defaults()
