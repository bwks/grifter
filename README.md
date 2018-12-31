# Grifter
Python library to build large scale Vagrant topologies for the networking 
space. Can also be used the build small scale labs for networking/compute 
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
A command line utility for managing the lifecycle of virtual machines
```

## Vagrant Libvirt
What is Vagrant Libvirt? From the `vagrant-libvirt` github [page](https://github.com/vagrant-libvirt/vagrant-libvirt) 
```
A Vagrant plugin that adds a Libvirt provider to Vagrant, allowing Vagrant to control and provision machines via Libvirt toolkit.
```

## Why
When simulating large topologies Vagrantfiles can become thousands 
of lines long. Getting all the configuration correct is often a 
frustrating, error riddled process especially for those not familiar 
with Vagrant. Grifter aims to help simplify that process.

##### Additional project goals
- Generate topology.dot files for use with PTM :heavy_check_mark:
- Generate Inventory files for tools such as Ansible, Nornir

NOTE: Only a `vagrant-libvirt` compatible `Vagrantfile` for 
Vagrant version `>= 2.1.0` will be generated. 

Support for Virtualbox or any other provider type is not supported or
on the road map.

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
# Install the master branch.
pip install https://github.com/bobthebutcher/grifter/archive/master.zip
```

Releases are distributed via Github Releases.
```
# Install the latest release.
pip install https://github.com/bobthebutcher/grifter/archive/v0.2.11.zip
```

## Quick Start
Create a `guests.yml` file.
``` 
tee guests.yml > /dev/null << "EOF"
srv01:
  vagrant_box: 
    name: "centos/7"
EOF
```

Generate a Vagrantfile
``` 
grifter create guests.yml
```

Let Vagrant do its magic
``` 
vagrant up
```



## Config File
A file named `config.yml` is required to define the base settings of 
each box managed within the grifter environment. The default `config.yml` 
file can be found [here](grifter/config.yml)

### Box Naming
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

#### guest_config
The `guest_config` section defines characteristics about the Vagrant boxes 
used with grifter.
#### Required Parameters.
- data_interface_base
- data_interface_offset
- max_data_interfaces
- management_interface

Note: `data_interface_base` cannot be an empty string. If the box does not 
have any data interfaces the suggested value is "NA". This field will be 
ignored so it can be anything as long as it is not empty.

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

#### guest_pairs
The `guest_pairs` section is used the define boxes that need two VMs to 
be fully functional. Some examples are the Juniper vMX and vQFX where 
one box is used for the control-plane and another for the forwarding-plane.

NOTE: This functionality will be added in a future release.

#### Custom config files
A default config file ships with the grifter python package.
This file can be customized with your required parameters by creating a 
`config.yml` file in the following locations.
 - `/opt/grifter/`
 - `~/.grifter/`
 - `./` 
 
 Parameters in a users `config.yml` file will be merged with the default 
 `config.yml` file with the user-defined parameters taking preference.

## Usage

#### CLI Utility
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

#### Create Vagrantfile
```
grifter create guests.yml
```

### Guests Datafile
Guest VMs characteristics and interface connections are defined in a YAML file. 
This file can be named anything, but the recommended naming convention is 
`guests.yml`.

#### Guest Schema
Jinja2 is used a the templating engine to generate the Vagrantfiles.
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
    throttle_cpu: # integer - optional | default: 0

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

#### Example Datafile
The following example datafile defines two `arista/veos` switches connected 
together on ports 1 and 2.
```yaml
sw01:
  vagrant_box:
    name: "arista/veos"
    version: "4.20.1F"
    guest_type: "tinycore"
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
    version: "4.20.1F"
    guest_type: "tinycore"
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
domain_uuid = "1f22b55d-2d7e-5a24-b4fa-3a8878df5cc5"

Vagrant.require_version ">= 2.1.0"
Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    guest_name = "sw01"
    node.vm.box = "arista/veos"
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :tinycore
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 2
      domain.memory = 2048
      domain.disk_bus = "ide"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw01-eth1 <--> sw02-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.146.53.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.146.53.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw01-eth1-#{domain_uuid}",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth2 <--> sw02-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.146.53.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.146.53.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw01-eth2-#{domain_uuid}",
      auto_config: false

  end
  config.vm.define "sw02" do |node|
    guest_name = "sw02"
    node.vm.box = "arista/veos"
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :tinycore
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 2
      domain.memory = 2048
      domain.storage_pool_name = "disk1"
      domain.disk_bus = "ide"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw02-eth1 <--> sw01-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.146.53.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.146.53.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw02-eth1-#{domain_uuid}",
      auto_config: false

    node.vm.network :private_network,
      # sw02-eth2 <--> sw01-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.146.53.2",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.146.53.1",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw02-eth2-#{domain_uuid}",
      auto_config: false

  end

end
```

### Defaults Per-Guest Type
It is possible to define default values per guest group type. Grifter will 
look for a file named `guest-defaults.yml` in the following locations from 
the least to most preferred:

 - `/opt/grifter/`
 - `~/.grifter/`
 - `./` 

```yaml
arista/veos:
  vagrant_box:
    version: "4.20.1F"
    guest_type: "tinycore"
  ssh:
    insert_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 24
    cpus: 2
    memory: 2048
    disk_bus: "ide"

juniper/vsrx-packetmode:
  vagrant_box:
    version: "18.3R1-S1.4"
    provider: "libvirt"
    guest_type: "tinycore"
  ssh:
    insert_key: False
  synced_folder:
    enabled: False
  provider_config:
    nic_adapter_count: 2
    disk_bus: "ide"
    cpus: 2
    memory: 4096
```

Group variables can be over-written by variables at the guest variable level. 
The values of the group and guest variables will be merged prior to building 
a `Vagrantfile` with the guest variables taking precedence over the group 
variables.

This means you can have a much more succinct guests file by reducing 
a lot of duplication. Here is an example of a simplified guest file. The 
values from the `arista/veos` guest type in the `guest-defaults.yml` file 
will be used to fill in the parameters for the guests.

```yaml
sw01:
  vagrant_box:
    name: "arista/veos"
  provider_config:
    nic_adapter_count: 2
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
  data_interfaces:
    - local_port: 1
      remote_guest: "sw01"
      remote_port: 1
    - local_port: 2
      remote_guest: "sw01"
      remote_port: 2
```

The generated `Vagrantfile` below is the same as the one above, but with a 
much cleaner guest definition file.

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
domain_uuid = "d35fb1b6-ecdc-5412-be22-185446af92d6"

Vagrant.require_version ">= 2.1.0"
Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    guest_name = "sw01"
    node.vm.box = "arista/veos"
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :tinycore
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 2
      domain.memory = 2048
      domain.disk_bus = "ide"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw01-eth1 <--> sw02-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.127.145.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.127.145.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw01-eth1-#{domain_uuid}",
      auto_config: false

    node.vm.network :private_network,
      # sw01-eth2 <--> sw02-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.127.145.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.127.145.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw01-eth2-#{domain_uuid}",
      auto_config: false

  end
  config.vm.define "sw02" do |node|
    guest_name = "sw02"
    node.vm.box = "arista/veos"
    node.vm.box_version = "4.20.1F"
    node.vm.guest = :tinycore
    node.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

    node.ssh.insert_key = false

    node.vm.provider :libvirt do |domain|
      domain.default_prefix = "#{domain_prefix}"
      domain.cpus = 2
      domain.memory = 2048
      domain.storage_pool_name = "disk1"
      domain.disk_bus = "ide"
      domain.nic_adapter_count = 2
    end

    node.vm.network :private_network,
      # sw02-eth1 <--> sw01-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.127.145.2",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.127.145.1",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw02-eth1-#{domain_uuid}",
      auto_config: false

    node.vm.network :private_network,
      # sw02-eth2 <--> sw01-eth2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.127.145.2",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.127.145.1",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "sw02-eth2-#{domain_uuid}",
      auto_config: false

  end

end
```

## Example Files
Examples of the `config.yml`, `guests-defaults.yml` and `guests.yml` files 
can be found [here](grifter/examples)


## Interfaces
There are 3 types of interfaces that can be defined.

- internal_interfaces
- data_interfaces
- reserved_interfaces

#### Internal Interfaces
Config location: `guests.yml`  
Used for an inter-vm communication channel for multi-vm boxes.  
Known examples are the vMX and vQFX.

#### data_interfaces
Config location: `guests.yml`  
Revenue ports that are used to pass data traffic.

#### reserved_interfaces
Config location: `config.yml`  
Interfaces that need to be defined because 'reasons' but cannot be 
used. The only known example is the `juniper/vqfx-re`. The number of 
reserved_interfaces is defined per-box type in the `config.yml` file. 
Grifter builds out the interface definitions automatically as a 
blackhole interfaces.

#### Blackhole Interfaces
Interfaces defined in the Vagratfile relate to interfaces 
on the guest vm on a first to last basis. This can be undesirable when 
trying to accurately simulate a production environment when devices 
can have 48+ ports.  

Grifter will automatically create `blackhole interfaces` to fill out 
undefined `data_interfaces` ports up to the box types 
`max_data_interfaces` parameter in the `config.yml` file. 

#### Vagrantfile Interface Order
Interfaces are added to the Vagrantfile in the following order.
- internal_interfaces
- reserved_interfaces
- data_interfaces

Interfaces are configured using the udp tunneling type. This 
will create a 'pseudo' layer 1 connection between VM ports.

##### Example interface definition
```yaml
  data_interfaces:
    - local_port: 1
      remote_guest: "sw02"
      remote_port: 1
```
##### Rendered Vagrantfile interface
```ruby
    node.vm.network :private_network,
      # sw01-eth1 <--> sw02-eth1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.255.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.255.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "sw01-eth1-#{domain_uuid}",
      auto_config: false
```

#### NIC Adapter Count
Config location: `guests.yml`  
Defines the total number of `data_interfaces` to create on the VM. 
Any undefined `data_interfaces` will be added as a blackhole interface.

The total is calculated against the sum of the `internal_interfaces`, `
reserved_interfaces` and `data_interfaces` parameters after blackhole 
interfaces have been added automatically by the template system.
