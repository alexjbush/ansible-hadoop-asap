from ansible import errors
import crypt

def hashpass(password):
	return crypt.crypt(password,'\$6\$\$')

class FilterModule(object):
	''' Filter plugin for hashing a password for use in user module '''
	def filters(self):
		return {
			'hashpass': hashpass
		}
