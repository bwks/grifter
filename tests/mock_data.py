mock_guest_data = {
  'guests': [
    {
      'insert_ssh_key': False,
      'interfaces': [
        {
          'local_port': 1,
          'name': 'eth1',
          'remote_host': 'sw02',
          'remote_port': 1
        },
        {
          'local_port': 2,
          'name': 'eth2',
          'remote_host': 'sw02',
          'remote_port': 2
        }
      ],
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
        'version': ''
      }
    },
    {
      'insert_ssh_key': False,
      'interfaces': [
        {
          'local_port': 1,
          'name': 'eth1',
          'remote_host': 'sw01',
          'remote_port': 1
        },
        {
          'local_port': 2,
          'name': 'eth2',
          'remote_host': 'sw01',
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
        'version': ''
      }
    }
  ]
}

mock_guest_interfaces = mock_guest_data['guests'][0]['interfaces']

with open('mock_vagrantfile.rb', 'r') as f:
    mock_vagrantfile = f.read()
