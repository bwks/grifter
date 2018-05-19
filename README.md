# vagrant-topology-builder
Python library to build large scale Vagrant topologies for the networking space, but can also be used the build small scale labs for non-networking devices.

Note: Python 3.6+ is supported.

```
*****************************************************************
This project is in beta and stability is not currently guaranteed
Breadking API changes can be expected
*****************************************************************
```


The main goal of this project is to build Vagrant topologies from yaml files.
As a secondary objective I would like to also generate graphviz dot files as well.
Currently only a vagrant-libvirt compatible Vagrantfile will be generated.

[![Build Status](https://travis-ci.org/bobthebutcher/vagrant-topology-builder.svg?branch=master)](https://travis-ci.org/bobthebutcher/vagrant-topology-builder)
[![Coverage Status](https://coveralls.io/repos/github/bobthebutcher/vagrant-topology-builder/badge.svg?branch=master)](https://coveralls.io/github/bobthebutcher/vagrant-topology-builder?branch=master)

#### Installation
Create and activate virtualenv. I will use pipenv for this example
as it is my preferred method for handling virtual evironments.
```
mkdir ~/test; cd ~/test
pipenv install
pipenv shell
```

Install `vagrant-topology-builder` with `pip`
```
pip install https://github.com/bobthebutcher/vagrant-topology-builder/archive/master.zip
```

#### Example Usage
```
vagrantfile create hosts.yml
```


#### Example Datafile
```yaml
---
guests:
  - name: "sw01"
    vagrant_box:
      name: "arista/veos"
      version: ""
      provider: "libvirt"

    insert_ssh_key: False
    synced_folder:
      enabled: False

    provider_config:
      nic_adapter_count: 2
      disk_bus: "ide"
      cpus: 2
      memory: 2048
      management_network_mac: ""

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
      version: ""
      provider: "libvirt"

    insert_ssh_key: False
    synced_folder:
      enabled: False

    provider_config:
      nic_adapter_count: 2
      disk_bus: "ide"
      cpus: 2
      memory: 2048
      management_network_mac: ""

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
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 2
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
    end

    node.vm.network :private_network,
      # sw01-int1 <--> sw02-int1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw01-int2 <--> sw02-int2
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
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 2
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
    end

    node.vm.network :private_network,
      # sw02-int1 <--> sw01-int1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw02-int2 <--> sw01-int2
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

#### Defaults Per-Guest Type
It is possible to defined default values per guest group type. The application will look for a
file name `guest-defaults.yml` in the current working directory that the `vagrantfile`
command is executed.
```yaml
arista/veos:
  vagrant_box:
    version: "4.20.1F"
    type: "other"
  insert_ssh_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 8
    disk_bus: "ide"
    cpus: 2
    memory: 2048

juniper/vsrx:
  vagrant_box:
    version: "18.1R1.9-packetmode"
    type: "other"
  insert_ssh_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 8
    disk_bus: "ide"
    cpus: 2
    memory: 4096
```

Group variables can be over-written by variables at the guest variable level. The values of
the group and guest variables will be merged prior to building a `Vagrantfile` with the guest
variables taking precedence over the group variables.


This means you can have a much more succinct guests variable file by reducing alot of duplication.
Here is an example of a reduced guest variable file.
```yaml
guests:
  - name: "sw01"
    vagrant_box:
      name: "arista/veos"

    provider_config:
      nic_adapter_count: 2
      management_network_mac: "00:00:00:00:00:01"

    interfaces:
      - name: "eth1"
        local_port: 1
        remote_guest: "sw02"
        remote_port: 1
      - name: "eth2"
        local_port: 2
        remote_guest: "sw02"
        remote_port: 2

  - name: "sw02"
    vagrant_box:
      name: "arista/veos"

    provider_config:
      nic_adapter_count: 2
      management_network_mac: "00:00:00:00:00:02"

    interfaces:
      - name: "eth1"
        local_port: 1
        remote_guest: "sw01"
        remote_port: 1
      - name: "eth2"
        local_port: 2
        remote_guest: "sw01"
        remote_port: 2
```

The resulting `Vagrantfile` is as follows
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
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :other
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 2
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
      domain.management_network_mac = "00:00:00:00:00:01"
    end

    node.vm.network :private_network,
      # sw01-int1 <--> sw02-int1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw01-int2 <--> sw02-int2
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
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :other
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.nic_adapter_count = 2
      domain.disk_bus = "ide"
      domain.cpus = 2
      domain.memory = 2048
      domain.management_network_mac = "00:00:00:00:00:02"
    end

    node.vm.network :private_network,
      # sw02-int1 <--> sw01-int1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw02-int2 <--> sw01-int2
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