# -*- coding: utf-8 -*-

import time

from rust.core.exceptions import ApiNotExistError

APPRESOURCE2CLASS = dict()

class _ApiResourceBase(type):
	def __new__(cls, name, bases, attrs):
		return super(_ApiResourceBase, cls).__new__(cls, name, bases, attrs)

	def __init__(self, name, bases, attrs):
		if name == 'ApiResource':
			pass
		else:
			app_resource = '%s-%s' % (self.app, self.resource)

			for key, value in self.__dict__.items():
				if hasattr(value, '__call__'):
					static_method = staticmethod(value)
					setattr(self, key, static_method)

			APPRESOURCE2CLASS[app_resource] = {
				'cls': self,
				'instance': None
			}

		super(_ApiResourceBase, self).__init__(name, bases, attrs)

class ApiResource(object):
	__metaclass__ = _ApiResourceBase

class ApiLogger(object):

	@staticmethod
	def print_req(app, resource, method, data, time_start):
		print ('/{}/{}/{}?{} =>{}'.format(app, resource, method, data, time.clock() - time_start))

	@staticmethod
	def log(req_data, resp_data, mode):
		"""
		将api请求状态、参数、响应存入数据库
		@:param mode 模式：ALL、REQ、RESP、RESP_NO_DATA
		todo
		"""
		pass

def api_call(method, app, resource, data, req=None, resp=None):
	resource_name = resource
	key = '%s-%s' % (app, resource)
	start_at = time.clock()

	resource = APPRESOURCE2CLASS.get(key, None)
	if not resource:
		raise ApiNotExistError(app, resource, method)

	func = getattr(resource['cls'], method, None)
	if not func:
		raise ApiNotExistError(app, resource, method)

	data['__req'] = req
	data['__resp'] = resp
	response = func(data)
	del data['__req']
	del data['__resp']
	ApiLogger.print_req(app, resource_name, method, data, start_at)
	return response