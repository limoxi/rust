
class AsyncEvent(object):
	__slots__ = (
		'name',
		'tag',
		'data',
	)

	def __init__(self, name, tag=''):
		self.name = name
		self.tag = tag