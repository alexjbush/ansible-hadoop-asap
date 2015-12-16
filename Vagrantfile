# -*- mode: ruby -*-

# vi: set ft=ruby :
require 'open3'
require 'json'
stdin, stdout, stderr, wait_thr = Open3.popen3('python inventories/inventory.py --vagrant')
output = stdout.gets(nil)
stdout.close
err_output = stderr.gets(nil)
stderr.close
exit_code = wait_thr.value
if exit_code != 0
	puts "Error running dynamic inventory:\n"+err_output
	exit 1
end
boxes = JSON.parse(output)

Vagrant.configure(2) do |config|

  config.vm.box = "puppetlabs/centos-6.6-64-nocm"

  # Turn off shared folders
  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true

  boxes.each do |host, opts|
    config.vm.define host do |config|
      config.vm.hostname = host

      config.vm.provider "vmware_fusion" do |v|
        v.vmx["memsize"] = opts["mem"]
        v.vmx["numvcpus"] = opts["cpu"]
      end

      config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", opts["mem"]]
        v.customize ["modifyvm", :id, "--cpus", opts["cpu"]]
      end

      config.vm.network :private_network, ip: opts["ip"]
    end
  end
end
