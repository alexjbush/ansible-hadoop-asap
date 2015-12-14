#!/bin/python
from __future__ import print_function
import optparse,json,sys,os,ConfigParser,pprint

#Dynamic wrapper for clusters

def parse_opts():
	parser = optparse.OptionParser()
	parser.add_option("--list", dest="list", default=False, action="store_true",
		help="List groups and hosts in groups")
	parser.add_option("--host", dest="host", help="Details for a given host", metavar='HOST')
	(options, args) = parser.parse_args()
	if options.list and options.host:
		print('Please only specify one commandline argument')
		parser.print_help()
		sys.exit(1)
	if options.list:
		return('list','')
	elif options.host:
		return('host',options.host)
	else:
		print('Please specify an action')
		parser.print_help()
		sys.exit(1)

def read_config():
	python_file = os.path.dirname(os.path.realpath("__file__"))+'/'+__file__
	if not python_file.endswith('.py'):
		print('ERROR: this script must end with .py')
		sys.exit(1)
	config_file = python_file[:-3]+'.cfg'
	if not os.path.exists(config_file):
		print('ERROR: config file could not be found: '+config_file)
		sys.exit(1)
	config = ConfigParser.RawConfigParser()
	config.read(config_file)
	configs=dict()
	configs['database_file'] = os.path.dirname(os.path.realpath("__file__"))+'/'+           \
				   os.path.dirname(__file__)+'/'+config.get('default','database')
	return configs

def inventory_consistency_check(inventory):
	pass

def load_db(config):
	if not os.path.exists(config['database_file']):
		print('ERROR: cannot read database file: '+config['database_file'])
		sys.exit(1)
	file = open(config['database_file'],'r')
	database = json.load(file)
	file.close()
	inventory_consistency_check(database)
	return database

def main():
	config = read_config()
	inventory = load_db(config)
	action,arg = parse_opts()
	print('Action: '+action+' Arg: '+arg)
	pprint.pprint(inventory)

if __name__ == '__main__':
	main()

