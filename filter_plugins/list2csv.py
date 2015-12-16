from ansible import errors

def list2csv(items,sep=','):
	try:
		csv = sep.join(items)
	except:
		raise errors.AnsibleFilterError('Cannot convert list to csv: '+str(items) +' with seperator: '+sep)
	return csv

class FilterModule(object):
	''' Filter plugin for converting list to csv '''
	def filters(self):
		return {
			'list2csv': list2csv
		}
