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
      domain.storage :file, :path => "/fake/location/volume1.qcow2", :size => "10000", :type => "qcow2", :bus => "ide", :device => "hdb", :allow_existing => true
      domain.storage :file, :path => "/fake/location/volume2.img", :size => "10000", :type => "raw", :bus => "ide", :device => "hdc", :allow_existing => true
    end
    add_volumes = [
      "virsh vol-create-as default #{username}-#{guest_name}-volume1.qcow2 10000",
      "sleep 1",
      "virsh vol-upload --pool default #{username}-#{guest_name}-volume1.qcow2 /fake/location/volume1.qcow2",
      "sleep 1",
      "virsh vol-create-as default #{username}-#{guest_name}-volume2.img 10000",
      "sleep 1",
      "virsh vol-upload --pool default #{username}-#{guest_name}-volume2.img /fake/location/volume2.img",
      "sleep 1"
    ]
    add_volumes.each_with_index do |value, index|
      node.trigger.before :up do |trigger|
        trigger.name = "add-volumes-#{index + 1}"
        trigger.info = "Adding Volumes #{index + 1}"
        trigger.run = {inline: value}
      end
    end

    delete_volumes = [
      "virsh vol-delete #{username}-#{guest_name}-volume1.qcow2 default",
      "virsh vol-delete #{username}-#{guest_name}-volume2.img default"
    ]
    delete_volumes.each_with_index do |value, index|
      node.trigger.after :destroy do |trigger|
        trigger.name = "remove-volumes-#{index + 1}"
        trigger.info = "Removing Volumes #{index + 1}"
        trigger.run = {inline: value}
      end
    end

    node.vm.network :private_network,
      # sw01-int1 <--> sw02-int1
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.255.1",
      :libvirt__tunnel_local_port => 10001,
      :libvirt__tunnel_ip => "127.255.255.2",
      :libvirt__tunnel_port => 10001,
      :libvirt__iface_name => "eth1",
      auto_config: false

    node.vm.network :private_network,
      # sw01-int2 <--> sw02-int2
      :mac => "#{get_mac()}",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.255.255.1",
      :libvirt__tunnel_local_port => 10002,
      :libvirt__tunnel_ip => "127.255.255.2",
      :libvirt__tunnel_port => 10002,
      :libvirt__iface_name => "eth2",
      auto_config: false

  end

end