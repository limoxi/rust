# -*- coding: utf-8 -*-

from datetime import datetime

INSTANCE = None

class Event(object):
	"""
	领域事件服务
	暂只是同步方式
	"""
	@classmethod
	def get(cls):
		global INSTANCE
		if not INSTANCE:
			INSTANCE = cls()
		
		return INSTANCE

	def __init__(self):
		self.event2handlers = {}

	def register(self, event, handler):
		"""
		注册event的handler
		"""
		self.event2handlers.setdefault(event, []).append(handler)

	def emit(self, event, data):
		"""
		触发event
		"""
		handlers = self.event2handlers.get(event)
		if not handlers:
			print 'no handlers for event [{}]'.format(event)
			return

		data['_time'] = datetime.now().strftime('%Y%m%d%H%M%S')

		for handler in handlers:
			handler(data)

def event_handler(event):
	"""
	使用event_handler向EventBus注册事件处理器

	@event_handler('event1')
	def event1_handler(event, data):
		...
		pass
	"""
	def wrapper(function):
		function.__name__ = '%s__%s' % (function.__module__, event)
		Event.get().register(event, function)

	return wrapper