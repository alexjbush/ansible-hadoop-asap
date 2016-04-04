# ansible-hadoop-asap
> “ASAP. Whatever that means. It must mean, 'Act swiftly awesome pachyderm!'”

Ansible Playbooks to install Hortonworks Data Platform (HDP) using Ambari Blueprints. Currently the Playbooks install an MIT KDC and resulting cluster is fully kerberised.

This has been tested against CentOS6 and CentOS7 in Vagrant.

##### Updates
* Kerberos now deployed optionally during blueprint build. Specify it as a service in: [group_var/all](group_vars/all) (Only available Ambari 2.2.1+ due to [AMBARI-14409](https://issues.apache.org/jira/browse/AMBARI-14409), use the old deployment method if a lower Ambari version is needed)
* Ranger now deployed as an optional service
* Ranger SSL now optional. Check ssl_services in [group_var/all](group_vars/all)
* Namenode HA now optional by specifying namenode in ha_services in [group_var/all](group_vars/all)

## Getting started
The inventory file is expected in be in a format similar to the example: [example](inventories/example_inventory).

All hosts must be in a _clustername_ group, in the appropriate _services_ group and a _clustername_service_ group.

Alternatively, you can use one of the instance creation methods below and use an included dynamic inventory (e.g. [inventory.py](inventories/vagrant/inventory.py)).

#### Creating instances

###### Vagrant
To use these scripts with Vagrant, change directory into [inventories/vagrant](inventories/vagrant), modify the [vagrant.json](inventories/vagrant/vagrant.json) file to your liking and run `vagrant up`. Make sure the hostnames are resolvable from the ansible host (hint: place entries in /etc/hosts).

You can choose the Vagrant box (Cent 6 or 7) by editing [inventory.cfg](inventories/vagrant/inventory.cfg).

#### Configuration
Most configuration is done through the [group_vars](group_vars) files.

For now, users can be configured in the [vars/users.yml](vars/users.yml) file and KDC credentials can be configured in the [vars/kdc_config](vars/kdc_config) file.

Services can be configured in the [group_vars/all](group_vars/all) file. Currently only Kerberos, Ranger, Spark, HBase, Oozie, Falcon, Storm and Kafka are optional services. All others are mandatory.

Ranger admin and admin<->plugins can now be optionally SSL'd by using setting ssl_services: [group_vars/all](group_vars/all)

#### Running the Playbook
```
ansible-playbook -i inventories/vagrant/inventory.py pb_provision_cluster.yml -e 'cluster_name=vagrantcluster'
```

#### Notes
Currently, users are managed in an OpenLDAP server and their credentials are stored in an MIT KDC. Unix authentication is done by SSSD using KDC5.

## TO DO
- [ ] Build blueprints dynamically (j2) depending on services requested
- [ ] FreeIPA support (alternative to MIT KDC)
- [x] OpenLDAP when using KDC (no local users)
- [x] Ranger
- [ ] RangerKMS, Knox and other advanced services support
- [ ] Pull implementations in [library](library/) modules to shared Ambari python class
- [x] CentOS 7 support
- [ ] AWS support
- [ ] OpenStack support
- [ ] Azure support
- [x] NTP


## [License](LICENSE)

Copyright (c) 2015 Alex Bush.  
Licensed under the [Apache License](LICENSE).
