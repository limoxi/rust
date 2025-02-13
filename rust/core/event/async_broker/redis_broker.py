
class RedisBroker(object):

	def send(self, event):
		print (event.data)