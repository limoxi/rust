
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
		RESOURCE2CLASS[self.resource] = klass
		print(f'load resource {self.resource}')
		return klass

class ApiResource(object):
	__slots__ = (
		'req',
		'resp',
		'params',
	)

	def __init__(self, req, resp, data):
		self.req = req
		self.resp = resp
		self.params = data


class ApiLogger(object):

	@staticmethod
	def print_req(resource, method, data, time_start):
		print (f'{resource}.{method.upper()} {(time.perf_counter() - time_start)*1000:.2f}ms {data}')

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
	start_at = time.perf_counter()

	resource_class = RESOURCE2CLASS.get(key, None)
	if resource_class is None:
		raise ApiNotExistError(resource, method)

	resource_inst = resource_class(req, resp, data)
	func = getattr(resource_inst, method, None)
	if not func:
		raise ApiNotExistError(resource, method)

	response = func()
	ApiLogger.print_req(resource_name, method, data, start_at)
	return response