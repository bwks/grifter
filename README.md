# vagrant-topology-builder
Python library to build Vagrant topologies. Python 3.6+ is supported.

The main goal of this project is to build Vagrant topologies from yaml files.
As a secondary objective I would like to also generate graphviz dot files as well.
Currently only a vagrant-libvirt compatible Vagrantfile will be generated.

#### Example Data
```yaml
---
hosts:
  - name: "sw01"
    vagrant_box:
      name: "arista/veos"
      version:
      provider:

    insert_ssh_key: False
    synced_folder:

    provider_config:
      nic_adapter_count: 12
      disk_bus: "ide"
      cpus: 2
      memory: 2048

    interfaces:
      - name: "eth1"
        local_port: 1
        remote_host: "sw02"
        remote_port: 1
      - name: "eth2"
        local_port: 2
        remote_host: "sw02"
        remote_port: 2

  - name: "sw02"
    vagrant_box:
      name: "arista/veos"
      version:
      provider:

    insert_ssh_key: False
    synced_folder:

    provider_config:
      nic_adapter_count: 12
      disk_bus: "ide"
      cpus: 2
      memory: 2048

    interfaces:
      - name: "eth1"
        local_port: 1
        remote_host: "sw01"
        remote_port: 1
      - name: "eth2"
        local_port: 2
        remote_host: "sw01"
        remote_port: 2
```

#### Generated Vagrantfile
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

def get_mac(oui="28:b7:ad")
  "Generate a MAC address"
  nic = (1..3).map{"%0.2x"%rand(256)}.join(":")
  return "#{oui}:#{nic}"
end

Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    node.vm.box = "arista/veos"

    node.ssh.insert_key = false

    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true


    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 12
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
    end
    node.vm.network :private_network,
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "eth2",
      auto_config: false

  end

  config.vm.define "sw02" do |node|
    node.vm.box = "arista/veos"

    node.ssh.insert_key = false

    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true


    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 12
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
    end
    node.vm.network :private_network,
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "eth2",
      auto_config: false

  end


end

```

#### Example Usage
Note: this will change slightly, its just a reminder to me at this point
```python
import yaml

from utils.custom_filters import explode_port
from utils.utils import generate_loopbacks
from utils.loaders import render_from_template

custom_filters = [explode_port]

with open('examples/hosts.yml', 'r') as f:
    data = yaml.load(f)

loopbacks = generate_loopbacks(data)

print(render_from_template('./templates', 'host.j2', custom_filters, hosts=data['hosts'], loopbacks=loopbacks))
```