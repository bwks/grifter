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

Vagrant.configure("2") do |config|

  config.vm.define "sw01" do |node|
    guest_name = "sw01"
    node.vm.box = "arista/veos"
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
    guest_name = "sw02"
    node.vm.box = "arista/veos"
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