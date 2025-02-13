import falcon
from falcon.routing import CompiledRouter

from rust import Config
from rust.core.db import db as rust_db
import importlib

from rust.core import api
from rust.core.exceptions import print_full_stack, ApiParameterError, ApiNotExistError, BusinessError
from rust.core.resp import ErrorResponse, JsonResponse
from rust.error_handlers.middleware_exception_handler import MiddlewareException

class FalconResource:
	def __init__(self):
		pass

	def __parse_api_params(self, req):
		params = {}
		params.update(req.params)
		params.update(req.context)
		params['api_id'] = req.path + '_' + req.method

		if req.method == 'POST':
			if 'text/plain' not in req.content_type:
				params.update(req.get_media())

		return params

	def __call(self, method, resource, req, params, resp):
		try:
			response = api.api_call(method, resource, params, req, resp)
			response = JsonResponse(response)
		except ApiNotExistError as e:
			response = ErrorResponse.get_from_exception(e)
		except ApiParameterError as e:
			response = ErrorResponse.get_from_exception(e)
		except BusinessError as e:
			response = ErrorResponse.get_from_exception(e)
		except Exception:
			print_full_stack()
			response = ErrorResponse(
				code=533,
				errMsg='系统错误',
			)

		return response

	def __call_api(self, method, resource, req, resp):
		req.context['_resource'] = resource
		resp.status = falcon.HTTP_200

		params = self.__parse_api_params(req)
		if rust_db is None:
			response = self.__call(method, resource, req, params, resp)
		else:
			with rust_db.manual_transaction() as transaction:
				response = self.__call(method, resource, req, params, resp)
				if response and response.code == 200:
					transaction.commit()
				else:
					transaction.rollback()

		resp.text = response.to_string()

	def on_get(self, req, resp, resource):
		self.__call_api('get', resource, req, resp)

	def on_put(self, req, resp, resource):
		self.__call_api('put', resource, req, resp)

	def on_post(self, req, resp, resource):
		_method = req.params.get('_method', 'post')
		self.__call_api(_method, resource, req, resp)

	def on_delete(self, req, resp, resource):
		self.__call_api('delete', resource, req, resp)

def __load_middlewares():
	"""
	加载中间件
	"""
	middlewares = []
	for middleware in Config.get_list('rust.middleware.middlewares'):
		items = middleware.split('.')
		module_path = '.'.join(items[:-1])
		module_name = items[-1]
		module = importlib.import_module(module_path)
		klass = getattr(module, module_name, None)
		if klass:
			print ('load middleware {}'.format(middleware))
			middlewares.append(klass())
		else:
			print ('[ERROR]: invalid middleware {}'.format(middleware))
	return middlewares

class __ResourceRouter(CompiledRouter):
	"""
	定制router匹配策略
	"""
	def find(self, uri, req=None):
		path = uri.lstrip('/').rstrip('/').replace('/', '.')
		params = {}
		node = self._find([path], self._return_values, self._patterns,
						  self._converters, params)

		if node is not None:
			return node.resource, node.method_map, params, node.uri_template
		else:
			return None

def create_app():
	middlewares = __load_middlewares()
	router = __ResourceRouter()
	falcon_app = falcon.App(middleware=middlewares, router=router)

	# 解析值为空的参数
	falcon_app.req_options.keep_blank_qs_values = True

	# 注册到Falcon
	falcon_app.add_route('/{resource}', FalconResource())

	#加载错误处理器
	falcon_app.add_error_handler(MiddlewareException)

	return falcon_app