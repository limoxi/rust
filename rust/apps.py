# -*- coding: utf-8 -*-

import json
import falcon
from falcon.routing import BaseConverter, CompiledRouter

from rust.core.db import db as rust_db

from rust.core import api
from rust.core.exceptions import unicode_full_stack, ApiParameterError, ApiNotExistError, BusinessError
from rust.core.api import ApiLogger
from rust.core.resp import ErrorResponse, JsonResponse
from rust.error_handlers.middleware_exception_handler import MiddlewareException

try:
	import settings
except:
	raise RuntimeError('[start server failed]: a py file named settings in the project root dir needed !!!]')

class FalconResource:
	def __init__(self):
		pass

	def __parse_api_params(self, req):
		"""
		对于不支持的content_type，直接返回空串
		"""
		params = {}
		params.update(req.params)
		params.update(req.context)
		params['api_id'] = req.path + '_' + req.method

		if req.method not in ['POST', 'PUT', 'DELETE']:
			return params
		content_type = req.content_type
		if content_type == falcon.MEDIA_JSON.split(';')[0] or (len(content_type.split(';')) > 1 and \
				content_type.split(';')[0] == falcon.MEDIA_JSON.split(';')[0]):
			params.update(json.loads(req.stream.read()))
		elif 'application/x-www-form-urlencoded' in content_type:
			pass
		elif content_type == falcon.MEDIA_XML:
			params['xml'] = req.stream.read()
		elif not content_type:
			params = None
		else:
			params = None

		return params

	def __call_api(self, method, resource, req, resp):
		req.context['_resource'] = resource
		resp.status = falcon.HTTP_200

		trx_rolled_back = False
		with rust_db.atomic() as transaction:
			response = None
			try:
				params = self.__parse_api_params(req)
				if not params:
					# 对于不支持的content_type，直接返回空串
					resp.body = ''
					return

				response = api.api_call(method, resource, params, req, resp)
				response = JsonResponse(response)
			except ApiNotExistError as e:
				response = ErrorResponse.get_from_exception(e)
			except ApiParameterError as e:
				response = ErrorResponse.get_from_exception(e)
			except BusinessError as e:
				response = ErrorResponse.get_from_exception(e)
			except Exception:
				error_stacks = unicode_full_stack()
				print (error_stacks)
				response = ErrorResponse(
					code = 533,
					errMsg = u'系统错误',
					innerErrMsg = error_stacks
				)
			finally:
				if response and response.code != 200:
					transaction.rollback()
					trx_rolled_back = True

		# 关闭数据库连接
		rust_db.close()

		if not trx_rolled_back:
			# 如果数据库事务已提交，则发送所有异步消息
			pass

		if settings.MODE == 'deploy' and response.code != 200:
			# 生产环境不对外保留错误堆栈
			response.innerErrMsg = ''

		resp.body = response.to_string()

		if hasattr(settings, 'API_LOGGER_MODE'):
			ApiLogger.log(req_data={
				'resource': resource,
				'method': method,
				'params': params,
				'req_instance': req
			}, resp_data={
				'resp_instance': resp
			}, mode=getattr(settings, 'API_LOGGER_MODE', None))

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
	for middleware in settings.MIDDLEWARES:
		items = middleware.split('.')
		module_path = '.'.join(items[:-1])
		module_name = items[-1]
		module = __import__(module_path, {}, {}, ['*', ])
		klass = getattr(module, module_name, None)
		if klass:
			print ('load middleware {}'.format(middleware))
			middlewares.append(klass())
		else:
			print ('[ERROR]: invalid middleware {}'.format(middleware))
	return middlewares

def load_resources():
	"""
	加载资源
	"""
	#加载rust资源
	if hasattr(settings, 'RUST_RESOURCES'):
		for resource in settings.RUST_RESOURCES:
			__import__('rust.resources.api.{}'.format(resource), {}, {}, ['*', ])
			print ('load rust built-in resource: {}'.format(resource))
	#加载用户定义的资源
	try:
		import api.resources
	except:
		print (unicode_full_stack())

class __ResourceRouter(CompiledRouter):
	"""
	定制router匹配策略
	"""
	def find(self, uri, req=None):
		if not uri.startswith('/static/'):
			path = [uri.lstrip('/').replace('/', '.')]
		else:
			path = uri.lstrip('/').split('/')
		params = {}
		node = self._find(path, self._return_values, self._patterns,
						  self._converters, params)

		if node is not None:
			return node.resource, node.method_map, params, node.uri_template
		else:
			return None

def create_app():
	load_resources()
	middlewares = __load_middlewares()
	router = __ResourceRouter()
	falcon_app = falcon.API(middleware=middlewares, router=router)

	# 解析值为空的参数
	falcon_app.req_options.keep_blank_qs_values = True

	# 解析formdata
	falcon_app.req_options.auto_parse_form_urlencoded = True

	# 注册到Falcon
	falcon_app.add_route('/{resource}/', FalconResource())

	#加载中间件错误处理器
	falcon_app.add_error_handler(MiddlewareException)

	if settings.DEBUG or getattr(settings, 'ENABLE_CONSOLE', False):
		from rust.dev_resource import service_console_resource
		falcon_app.add_route('/console/', service_console_resource.ServiceConsoleResource())

		from rust.dev_resource import static_resource
		falcon_app.add_sink(static_resource.serve_static_resource, '/static/')

	return falcon_app