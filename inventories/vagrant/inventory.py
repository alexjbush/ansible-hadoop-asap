#!/usr/bin/python
from __future__ import print_function
import optparse,json,sys,os,ConfigParser,pprint

#Dynamic wrapper for clusters

def parse_opts():
	parser = optparse.OptionParser()
	parser.add_option("--list", dest="list", default=False, action="store_true",
		help="List groups and hosts in groups")
	parser.add_option("--vagrant", dest="vagrant", default=False, action="store_true",
		help="Output vagrant file syntax")
	parser.add_option("--hosts-file", dest="hosts_file", default=False, action="store_true",
		help="Output hosts file listing of hosts")
	parser.add_option("--host", dest="host", help="Details for a given host", metavar='HOST')
	(options, args) = parser.parse_args()
	#if options.list and options.host:
	if sum([1 for opt in [options.list, options.vagrant, options.host, options.hosts_file] if opt]) > 1:
		print('Please only specify one commandline argument',file=sys.stderr)
		parser.print_help()
		sys.exit(1)
	if options.list:
		return('list','')
	elif options.host:
		return('host',options.host)
	elif options.vagrant:
		return('vagrant','')
	elif options.hosts_file:
		return('hosts_file','')
	else:
		print('Please specify an action',file=sys.stderr)
		parser.print_help()
		sys.exit(1)

def read_config():
	python_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.basename(__file__))
	python_file = os.path.expanduser(os.path.expandvars(python_file))
	if not python_file.endswith('.py'):
		print('ERROR: this script must end with .py',file=sys.stderr)
		sys.exit(1)
	config_file = python_file[:-3]+'.cfg'
	if not os.path.exists(config_file):
		print('ERROR: config file could not be found: '+config_file,file=sys.stderr)
		sys.exit(1)
	config = ConfigParser.RawConfigParser()
	try:
		config.read(config_file)
	except:
		print('ERROR: config file could not be read: '+config_file,file=sys.stderr)
		sys.exit(3)
	configs=dict()
	configs['database_file'] = os.path.dirname(config_file)+'/'+config.get('default','database')
	def get_config_boolean(config_object,key,default=False):
		if config.has_option('default',key):
			value = config.getboolean('default',key)
		else:
			value = default
		return value
	configs['ignore_existing'] = get_config_boolean(config,'ignore_existing_host_variables')
	configs['group_by_cluster_name'] = get_config_boolean(config,'group_by_cluster_name')
	configs['prepend_group_with_cluster_name'] = get_config_boolean(config,'prepend_groups_by_cluster_name')
	host_vars=['ansible_ssh_user','ansible_ssh_private_key_file','vagrant_box']
	configs['host_vars']=dict()
	for var in host_vars:
		if config.has_option('default',var):
			configs['host_vars'][var] = config.get('default',var)
	return configs

def inventory_consistency_check(inventory):
	pass

def load_db(config):
	if not os.path.exists(config['database_file']):
		print('ERROR: cannot read database file: '+config['database_file'],file=sys.stderr)
		sys.exit(1)
	try:
		dbfile = open(config['database_file'],'r')
	except:
		print('ERROR: cannot read database file: '+config['database_file'],file=sys.stderr)
		exit(3)
	database = json.load(dbfile)
	dbfile.close()
	inventory_consistency_check(database)
	for host in database['hosts'].keys():
		for host_var, host_var_val in config['host_vars'].iteritems():
			if not host_var in database['hosts'][host].keys() or config['ignore_existing']:
				database['hosts'][host][host_var] = host_var_val
	return database

def _add_host_to_group(groups,group_name,host):
	if not group_name in groups.keys():
		groups[group_name] = list()
		groups[group_name].append(host)
	elif type(groups[group_name]) is list:
		groups[group_name].append(host)
	else:
		groups[group_name]['hosts'].append(host)
	return groups

def _get_hosts_in_group(group):
	if type(group) is list:
		return group
	else:
		return group['hosts']

def list_action(inventory,configs):
	groups = inventory['groups']
	if configs['group_by_cluster_name'] or configs['prepend_group_with_cluster_name']:
		hosts = inventory['hosts']
		for host,hostvars in hosts.iteritems():
			if 'cluster_name' in hostvars.keys():
				cluster_name = hostvars['cluster_name']
				if configs['group_by_cluster_name']:
					groups = _add_host_to_group(groups,cluster_name,host)
				if configs['prepend_group_with_cluster_name']:
					for group in groups.keys():
						if not group.startswith(cluster_name) and host in _get_hosts_in_group(groups[group]):
							groups = _add_host_to_group(groups,cluster_name+'_'+group,host)
	print(json.dumps(groups,sort_keys=True,indent=4))

def host_action(inventory,host):
	hosts = inventory['hosts']
	if not host in hosts.keys():
		print('Host not found in hostlist',file=sys.stderr)
		sys.exit(1)
	print(json.dumps(hosts[host],sort_keys=True,indent=4))

def vagrant_action(inventory):
	hosts = inventory['hosts']
	print(json.dumps(hosts,sort_keys=True,indent=4))

def hosts_file_action(inventory):
	hosts = inventory['hosts']
	for host,hostvars in hosts.iteritems():
		if 'ip' in hostvars.keys():
			print(hostvars['ip']+' '+host)

def main():
	config = read_config()
	inventory = load_db(config)
	action,arg = parse_opts()
	if action == 'list':
		list_action(inventory,config)
	elif action == 'host':
		host_action(inventory,arg)
	elif action == 'vagrant':
		vagrant_action(inventory)
	elif action == 'hosts_file':
		hosts_file_action(inventory)

if __name__ == '__main__':
	main()

