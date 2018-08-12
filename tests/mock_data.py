from grifter.constants import TESTS_DIR

mock_guest_data = {
    'guests': [
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
                    'remote_guest': 'sw02',
                    'remote_port': 1
                },
                {
                    'local_port': 2,
                    'name': 'eth2',
                    'remote_guest': 'sw02',
                    'remote_port': 2
                }
            ],
            'name': 'sw01',
            'provider_config': {
                'random_hostname': False,
                'cpus': 2,
                'disk_bus': 'ide',
                'management_network_mac': '',
                'nic_model_type': '',
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
                'url': '',
                'guest_type': '',
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
                'nic_adapter_count': 2
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
            }
        }
    ]
}

mock_guest_interfaces = mock_guest_data['guests'][0]['interfaces']

with open(f'{TESTS_DIR}/mock_vagrantfile.rb', 'r') as f:
    mock_vagrantfile = f.read()


mock_invalid_guest_data_file = f'{TESTS_DIR}/mock_invalid_guest_data.yml'
