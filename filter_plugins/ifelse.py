from ansible import errors

def ifelse(conditional,restrue,resfalse):
	if conditional:
		return restrue
	else:
		return resfalse

class FilterModule(object):
	''' Filter plugin for if else '''
	def filters(self):
		return {
			'ifelse': ifelse
		}
