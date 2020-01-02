# -*- coding: utf-8 -*-

"""
领域事件通过装饰器event_handler注册，
但是需要自己import各处理模块
"""

from datetime import datetime

from async_event import AsyncEvent
from async_broker import console_broker, redis_broker, mns_broker

import settings

INSTANCE = None

class AsyncEventService(object):
	"""
	异步事件服务
	"""
	@classmethod
	def get(cls):
		global INSTANCE
		if not INSTANCE:
			INSTANCE = cls()
		
		return INSTANCE

	@staticmethod
	def make_event(name, tag=''):
		return AsyncEvent(name, tag)

	def __init__(self):
		self.async_events = []

	def __get_broker(self):
		"""
		获取异步消息处理器
		"""
		name = getattr(settings, 'EVENT_BROKER', 'console')
		if name == 'console':
			return console_broker.ConsoleBroker()
		elif name == 'redis':
			return redis_broker.RedisBroker()
		elif name == 'mns':
			return mns_broker.MnsBroker()

	def emit(self, event, data):
		"""
		触发event
		"""
		data['_time'] = datetime.now().strftime('%Y%m%d%H%M%S')
		event.data = data
		self.async_events.append(event)

	def send_all_async_events(self):
		"""
		按顺序发送所有异步消息
		这一方法必须在数据库事务提交后
		"""
		broker = self.__get_broker()
		if not broker:
			print 'no valid async broker exist'
			return
		for async_event in self.async_events:
			broker.send(async_event)