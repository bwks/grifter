# Grifter
Python library to build large scale Vagrant topologies for the networking 
space, but can also be used the build small scale labs for non-networking 
devices.

[![Build Status](https://travis-ci.org/bobthebutcher/grifter.svg?branch=master)](https://travis-ci.org/bobthebutcher/grifter.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/bobthebutcher/grifter/badge.svg?branch=master)](https://coveralls.io/github/bobthebutcher/grifter?branch=master)

NOTE: Python 3.6+ is required to make use of this library.

```
*****************************************************************
This project is currently in beta and stability is not currently 
guaranteed. Breaking API changes can be expected.
*****************************************************************

```
## Vagrant
What is Vagrant? From the Vagrant [website](https://www.vagrantup.com/docs/index.html)
```
The command line utility for managing the lifecycle of virtual machines
```

## Vagrant Libvirt
What is Vagrant Libvirt? From the `vagrant-libvirt` github [page](https://github.com/vagrant-libvirt/vagrant-libvirt) 
```
A Vagrant plugin that adds a Libvirt provider to Vagrant, 
allowing Vagrant to control and provision machines via Libvirt toolkit.
```

## Why
When simulating large topologies Vagrantfiles can become thousands 
of lines long. Getting all the configuration correct is often a 
frustrating, error riddled process especially for those not familiar 
with Vagrant. Grifter aims to help simplify that process.

##### Additional project goals
- Generate graphviz/PTM topologies files
- Generate Inventory files for tools such as Ansible, Nornir

NOTE: Currently only a `vagrant-libvirt` compatible Vagrantfile will be generated. 
Support for Virtualbox or any other provider type is not currently on the 
road map.

## Dependencies
Grifter requires the help of the following awesome projects from the Python 
community.
- [Cerberus](http://docs.python-cerberus.org/en/stable/) - Schema validation
- [Click](https://click.palletsprojects.com/) - CLI utility
- [Jinja2](http://jinja.pocoo.org/docs) - Template engine
- [PyYAML](https://pyyaml.org/) - YAML all the things

## Installation
There is currently no PyPI release for this project. Grifter can be 
installed directly from source using PIP. 

Create and activate virtualenv.
```
mkdir ~/test && cd ~/test
python3 -m venv .venv
source .venv/bin/activate
```

Install `grifter` with `pip`
```
pip install https://github.com/bobthebutcher/grifter/archive/master.zip
```

## Config File
A file named `config.yml` is required to define the base settings of 
each box managed within the grifter environment. The default `config.yml` 
file can be found [here](grifter/config.yml)

#### Box Naming
Grifter expects Vagrant boxes to be named according to the following list.

##### Custom Boxes
- arista/veos
- cisco/csr1000v
- cisco/iosv
- cisco/xrv
- juniper/vmx-vcp
- juniper/vmx-vfp
- juniper/vqfx-pfe
- juniper/vqfx-re
- juniper/vsrx
- juniper/vsrx-packetmode

##### Vagrant Cloud Boxes
- CumulusCommunity/cumulus-vx
- centos/7
- generic/ubuntu1804
- opensuse/openSUSE-15.0-x86_64

In a future release support will be added for boxes named according to user 
defined values.

##### guest_config
The `guest_config` section defines characteristics about the Vagrant boxes 
used with grifter.
##### Required Parameters.
- data_interface_base
- data_interface_offset
- max_data_interfaces
- management_interface

```yaml
guest_config:
  example/box:
    data_interface_base: "eth" # String pattern for data interfaces.
    data_interface_offset: 0 # Number of first data interface ie: 0, 1, 2, etc..
    internal_interfaces: 0 # Used for inter-box connections for multi-vm boxes.
    max_data_interfaces: 8 
    management_interface: "ma1"
    reserved_interfaces: 0 # Interfaces that are required but cannot be used.

  arista/veos:
    data_interface_base: "eth"
    data_interface_offset: 1
    internal_interfaces: 0
    max_data_interfaces: 24
    management_interface: "ma1"
    reserved_interfaces: 0

  juniper/vsrx-packetmode:
    data_interface_base: "ge-0/0/"
    data_interface_offset: 0
    internal_interfaces: 0
    max_data_interfaces: 16
    management_interface: "fxp0.0"
    reserved_interfaces: 0
```

##### guest_pairs
The `guest_pairs` section is used the define boxes that need two VMs to 
be fully functional. Some examples are the Juniper vMX and vQFX where 
one box is used for the control-plane and another for the forwarding-plane.

NOTE: This functionality wil be added in a future release.

##### Custom config files
A default config file ships with the grifter python package.
This file can be customized with your required parameters by creating a 
`config.yml` file in the following locations.
 - `/opt/grifter/`
 - `~/.grifter/`
 - `./` 
 
 Parameters in a users `config.yml` file will be merged with the default 
 `config.yml` file.

NOTE: This functionality wil be added in a future release.

## Usage

##### CLI Utility
Grifter ships with a CLI utility. Execute `grifter -h` to 
discover all the CLI options. 

```
grifter -h
Usage: grifter [OPTIONS] COMMAND [ARGS]...

  Create a Vagrantfile from a YAML data input file.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  create   Create a Vagrantfile.
  example  Print example file declaration.
```

##### Create Vagrantfile
```
grifter create guests.yml
```

#### Guests Datafile
Guest VMs are defined in a YAML file. This file can be named 
anything, but the recommended naming convention is `guests.yml`.

##### Guest Schema
Jinja2 is used a the templating engine to generate the Vagranfiles.
Guests definition within a guests file must use the following 
schema as it is required to ensure templates render correctly and 
without errors. The guest data will be validated against the schema 
using the Cerberus project.

```yaml
some-guest: # guest name
  vagrant_box: # vagrant_box parameters
    name: # string - required
    version: # string - optional | default: ""
    url: # string - optional | default: ""
    provider: # string - optional | default: "libvirt"
    guest_type: # string - optional | default: ""
    boot_timeout: # integer - optional | default: 0

  ssh: # dict - optional
    username: # string - optional | default: ""
    password: # string - optional | default: ""
    insert_key: # boolean - optional | default: False

  synced_folder: # dict - optional
    enabled: # boolean - default: False
    id: # string - default: "vagrant-root"
    src: # string - default: "."
    dst: # string - default: "/vagrant"

  provider_config: # dict - optional
    random_hostname: # boolean - optional | default: False
    nic_adapter_count: # integer - optional | default: 0
    disk_bus: # string - optional | default: ""
    cpus: # integer - optional | default: 1
    memory: # integer - optional | default: 512
    huge_pages: # boolean - optional | default: False
    storage_pool: # string - optional | default: ""
    additional_storage_volumes: # list - optional
      # For each list element the following is required.
      - location: # string
        type: # string
        bus: # string
        device: # string
    nic_model_type: # string - optional | default: ""
    management_network_mac: # string - optional | default: ""

  internal_interfaces: # list - optional
    # For each list element the following is required.
    - local_port: # integer
      remote_guest: # string
      remote_port: # integer

  data_interfaces: # list - optional
    # For each list element the following is required.
    - local_port: # integer
      remote_guest: # string
      remote_port: # integer
```


##### Example Datafile
```yaml
sw01:
  vagrant_box:
    name: "arista/veos"
    version: ""
    provider: "libvirt"
  ssh:
    insert_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 2
    disk_bus: "ide"
    cpus: 2
    memory: 2048
    management_network_mac: ""
  data_interfaces:
    - local_port: 1
      remote_guest: "sw02"
      remote_port: 1
    - local_port: 2
      remote_guest: "sw02"
      remote_port: 2

sw02:
  vagrant_box:
    name: "arista/veos"
    version: ""
    provider: "libvirt"
  ssh:
    insert_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 2
    disk_bus: "ide"
    cpus: 2
    memory: 2048
    management_network_mac: ""
  data_interfaces:
    - local_port: 1
      remote_guest: "sw01"
      remote_port: 1
    - local_port: 2
      remote_guest: "sw01"
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

cwd = Dir.pwd.split("/").last
username = ENV['USER']
domain_prefix = "#{username}_#{cwd}"

Vagrant.require_version ">= 2.1.0"
Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    guest_name = "sw01"
    node.vm.box = "arista/veos"
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 1
      domain.memory = 512
      domain.management_network_mac = "00:00:00:00:00:01"
      domain.nic_adapter_count = 8
    end

    node.vm.network :private_network,
      # sw01-eth1 <--> sw02-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw01-eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth2 <--> sw02-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw01-eth2",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth3 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10003,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth3",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth4 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10004,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth4",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth5 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10005,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth5",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth6 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10006,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth6",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth7 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10007,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth7",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth8 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10008,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth8",
      auto_config: false

  end
  config.vm.define "sw02" do |node|
    guest_name = "sw02"
    node.vm.box = "arista/veos"
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 1
      domain.memory = 512
      domain.management_network_mac = "00:00:00:00:00:02"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw02-eth1 <--> sw01-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw02-eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw02-eth2 <--> sw01-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw02-eth2",
      auto_config: false

  end

end
```

#### Defaults Per-Guest Type
It is possible to define default values per guest group type. Grifter will look for a
file named `guest-defaults.yml` in the following locations from the least to most preferred:
 - `/opt/grifter/`
 - `~/.grifter/`
 - `./` 

```yaml
arista/veos:
  vagrant_box:
    version: "4.20.1F"
  ssh:
    insert_key: False
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
  ssh:
    insert_key: False
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
sw01:
  vagrant_box:
    name: "arista/veos"

  provider_config:
    nic_adapter_count: 8
    management_network_mac: "00:00:00:00:00:01"

  data_interfaces:
    - local_port: 1
      remote_guest: "sw02"
      remote_port: 1
    - local_port: 2
      remote_guest: "sw02"
      remote_port: 2

sw02:
  vagrant_box:
    name: "arista/veos"

  provider_config:
    nic_adapter_count: 2
    management_network_mac: "00:00:00:00:00:02"

  data_interfaces:
    - local_port: 1
      remote_guest: "sw01"
      remote_port: 1
    - local_port: 2
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

cwd = Dir.pwd.split("/").last
username = ENV['USER']
domain_prefix = "#{username}_#{cwd}"

Vagrant.require_version ">= 2.1.0"
Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    guest_name = "sw01"
    node.vm.box = "arista/veos"
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 1
      domain.memory = 512
      domain.management_network_mac = "00:00:00:00:00:01"
      domain.nic_adapter_count = 8
    end

    node.vm.network :private_network,
      # sw01-eth1 <--> sw02-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw01-eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth2 <--> sw02-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw01-eth2",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth3 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10003,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth3",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth4 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10004,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth4",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth5 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10005,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth5",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth6 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10006,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth6",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth7 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10007,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth7",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth8 <--> blackhole-666
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.1",
      :libvirt__tunnel_local_port => 10008,
      :libvirt__tunnel_ip => "127.6.6.6",
      :libvirt__tunnel_port => 10666,
      :libvirt__iface_name => "sw01-eth8",
      auto_config: false

  end
  config.vm.define "sw02" do |node|
    guest_name = "sw02"
    node.vm.box = "arista/veos"
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 1
      domain.memory = 512
      domain.management_network_mac = "00:00:00:00:00:02"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw02-eth1 <--> sw01-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw02-eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw02-eth2 <--> sw01-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.1.2",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.1.1",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw02-eth2",
      auto_config: false

  end

end
```