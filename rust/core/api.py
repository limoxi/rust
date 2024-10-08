# coding: utf-8

import time

from rust.core.exceptions import ApiNotExistError

RESOURCE2CLASS = dict()

class Resource(object):
	"""
	资源装饰器
	"""
	def __init__(self, resource):
		self.resource = resource

	def __call__(self, klass):
		global RESOURCE2CLASS
		RESOURCE2CLASS[self.resource] = klass()
		return klass

class ApiResource(object):
	__slots__ = (
		'req',
		'resp',
		'params',
	)

	def init(self, req, resp, data):
		self.req = req
		self.resp = resp
		self.params = data

class ApiLogger(object):

	@staticmethod
	def print_req(resource, method, data, time_start):
		print ('/{}/{}?{} =>{}'.format(resource, method, data, time.clock() - time_start))

	@staticmethod
	def log(req_data, resp_data, mode):
		"""
		@:param mode 模式：ALL、REQ、RESP、RESP_NO_DATA
		todo
		"""
		pass

def api_call(method, resource, data, req=None, resp=None):
	resource_name = resource
	key = resource
	start_at = time.clock()

	resource = RESOURCE2CLASS.get(key, None)
	if not resource:
		raise ApiNotExistError(resource, method)

	func = getattr(resource, method, None)
	if not func:
		raise ApiNotExistError(resource, method)

	resource.init(req, resp, data)
	response = func()
	ApiLogger.print_req(resource_name, method, data, start_at)
	return response