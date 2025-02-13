
class ConsoleBroker(object):

	def send(self, event):
		print (event.data)