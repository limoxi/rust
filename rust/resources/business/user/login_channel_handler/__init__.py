# -*- coding: utf-8 -*-
__author__ = 'Asia'

REGISTERED_HANDLERS = dict()

class LoginChannelHandler(object):
	"""
	登录渠道装饰器
	"""
	def __init__(self, channel_name):
		self.channel_name = channel_name

	def __call__(self, klass):
		global REGISTERED_HANDLERS
		REGISTERED_HANDLERS[self.channel_name] = klass()
		return klass