mock_load_host_data = {
  'hosts': [
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
        'management_network_mac': None,
        'memory': 2048,
        'nic_adapter_count': 2
      },
      'synced_folder': None,
      'vagrant_box': {
        'name': 'arista/veos',
        'provider': 'libvirt',
        'version': None
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
        'management_network_mac': None,
        'memory': 2048,
        'nic_adapter_count': 2
      },
      'synced_folder': None,
      'vagrant_box': {
        'name': 'arista/veos',
        'provider': 'libvirt',
        'version': None
      }
    }
  ]
}