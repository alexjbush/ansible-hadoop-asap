# ansible-hadoop-asap
> “ASAP. Whatever that means. It must mean, 'Act swiftly awesome pachyderm!'”

Ansible Playbooks to install Hortonworks Data Platform (HDP) using Ambari Blueprints. Currently the Playbooks install an MIT KDC and resulting cluster is fully kerberised.

This has been tested against CentOS6 in Vagrant.

## Getting started
The inventory file is expected in be in a format similar to the example: [example](inventories/example_inventory).

All hosts must be in a _clustername_ group, in the appropriate _services_ group and a _clustername_service_ group.

Alternatively, you can use one of the instance creation methods below and use an included dynamic inventory (e.g. [inventory.py](inventories/vagrant/inventory.py)).

#### Creating instances

###### Vagrant
To use these scripts with Vagrant, change directory into [inventories/vagrant](inventories/vagrant), modify the [vagrant.json](inventories/vagrant/vagrant.json) file to your liking and run `vagrant up`. Make sure the hostnames are resolvable from the ansible host (hint: place entries in /etc/hosts).

#### Configuration
Most configuration is done through the [group_vars](group_vars) files.

For now, users can be configured in the [vars/users.yml](vars/users.yml) file and KDC credentials can be configured in the [vars/kdc_config](vars/kdc_config) file.

#### Running the Playbook
```
ansible-playbook -i inventories/vagrant/inventory.py pb_provision_cluster.yml -e 'cluster_name=vagrantcluster'
```

## TO DO
- [ ] Build blueprints dynamically (j2) depending on services requested
- [ ] FreeIPA support (alternative to MIT KDC)
- [ ] OpenLDAP when using KDC (no local users)
- [ ] Ranger, RangerKMS, Knox and other advanced services support
- [ ] Pull implementations in [library](library/) modules to shared Ambari python class
- [ ] CentOS 7 support (possibly Ubuntu)
- [ ] AWS support
- [ ] OpenStack support
- [ ] Azure support
- [x] NTP


## [License](LICENSE)

Copyright (c) 2015 Alex Bush.  
Licensed under the [Apache License](LICENSE).
