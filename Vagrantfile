# -*- mode: ruby -*-

# vi: set ft=ruby :

file = open("inventories/vagrant.json")
json = file.read
boxes = JSON.parse(json)

Vagrant.configure(2) do |config|

  config.vm.box = "puppetlabs/centos-6.6-64-nocm"

  # Turn off shared folders
  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

  boxes.each do |opts|
    config.vm.define opts["name"] do |config|
      config.vm.hostname = opts["name"]

      config.vm.provider "vmware_fusion" do |v|
        v.vmx["memsize"] = opts["mem"]
        v.vmx["numvcpus"] = opts["cpu"]
      end

      config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", opts["mem"]]
        v.customize ["modifyvm", :id, "--cpus", opts["cpu"]]
      end

      config.vm.network :private_network, ip: opts["eth1"]
    end
  end
end
