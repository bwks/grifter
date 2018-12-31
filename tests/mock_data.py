from grifter.constants import TESTS_DIR

mock_guest_data = {
    'sw01': {
        'ssh': {
            'username': '',
            'password': '',
            'insert_key': False,
        },
        'internal_interfaces': [],
        'reserved_interfaces': [],
        'data_interfaces': [
            {
                'local_port': 1,
                'remote_guest': 'sw02',
                'remote_port': 1
            },
            {
                'local_port': 2,
                'remote_guest': 'sw02',
                'remote_port': 2
            }
        ],
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
    },
    'sw02': {
        'ssh': {
            'username': '',
            'password': '',
            'insert_key': False,
        },
        'internal_interfaces': [],
        'reserved_interfaces': [],
        'data_interfaces': [
            {
                'local_port': 1,
                'remote_guest': 'sw01',
                'remote_port': 1
            },
            {
                'local_port': 2,
                'remote_guest': 'sw01',
                'remote_port': 2
            }
        ],
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

mock_guest_interfaces = mock_guest_data['sw01']['data_interfaces']

mock_additional_storage_volumes = [
    {
        'location': '/fake/location/volume1.qcow2',
        'type': 'qcow2',
        'bus': 'ide',
        'device': 'hdb',
    },
    {
        'location': '/fake/location/volume2.img',
        'type': 'raw',
        'bus': 'ide',
        'device': 'hdc',
    }
]


with open(f'{TESTS_DIR}/mock_vagrantfile.rb', 'r') as f:
    mock_vagrantfile = f.read()

with open(f'{TESTS_DIR}/mock_vagrantfile_additional_storage_volumes.rb', 'r') as f:
    mock_vagrantfile_with_additional_storage_volumes = f.read()

mock_invalid_guest_data_file = f'{TESTS_DIR}/mock_invalid_guest_data.yml'


mock_connection_data = [{'local_guest': 'sw1', 'local_port': 'swp7',
                         'remote_guest': 'r7', 'remote_port': 'ge-0/0/9'}]
