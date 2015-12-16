from ansible import errors

def uniquekeyvalues(data,key):
	def get_unique_key_values(data,key):
		values = set()
		if isinstance(data, dict):
			for dict_key,dict_value in data.iteritems():
				if key == dict_key:
					values.add(data[key])
				else:
					values = values | get_unique_key_values(dict_value,key)
		elif isinstance(data, list):
			for elem in data:
				values = values | get_unique_key_values(elem,key)
		return values
	return list(get_unique_key_values(data,key))
	#raise errors.AnsibleFilterError('Cannot convert list to csv: '+str(items) +' with seperator: '+sep)

class FilterModule(object):
	''' Filter plugin for getting unique key values from a complex data structure '''
	def filters(self):
		return {
			'uniquekeyvalues': uniquekeyvalues
		}
