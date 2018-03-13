# -*- coding: utf-8 -*-

import json
import falcon

from rust.core import api
from rust.core.exceptions import unicode_full_stack, ApiNotExistError
from rust.core.api import ApiLogger
from rust.core.resp import SystemErrorResponse, ResponseBase, JsonResponse

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

		if req.method != 'POST':
			return params

		content_type = req.content_type
		if content_type == falcon.MEDIA_JSON:
			params.update(json.loads(req.stream.read()))
		elif 'application/x-www-form-urlencoded' in content_type:
			pass
		elif content_type == falcon.MEDIA_XML:
			params['xml'] = req.stream.read()
			print '============'
			print params['xml']
		elif not content_type:
			raise RuntimeError('[request failed]: missing content_type !!!')
		else:
			params = None

		return params

	def __call_api(self, method, app, resource, req, resp):
		req.context['_app'] = app
		req.context['_resource'] = resource
		resp.status = falcon.HTTP_200
		
		try:
			params = self.__parse_api_params(req)
			if not params:
				# 对于不支持的content_type，直接返回空串
				resp.body = ''
				return

			response = api.api_call(method, app, resource, params, req, resp)
		except ApiNotExistError as e:
			response = SystemErrorResponse(
				code = 404,
				errMsg = str(e).strip(),
				innerErrMsg = 'api===>{}:{} not exist'.format(app, resource)
			)
		except Exception as e:
			response = SystemErrorResponse(
				code = 531,
				errMsg = str(e).strip(),
				innerErrMsg = unicode_full_stack()
			)

		if not isinstance(response, ResponseBase):
			response = JsonResponse(response)

		resp.body = response.to_string()

		ANY_HOST = '*'
		if hasattr(settings, 'CORS_WHITE_LIST'):
			valid_host = ''
			if len(getattr(settings, 'CORS_WHITE_LIST', [])) == 0:
				valid_host = ANY_HOST
			elif req.host in settings['CORS_WHITE_LIST']:
				valid_host = req.host

			if valid_host:
				resp.set_header("Access-Control-Allow-Origin", valid_host)
				resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

		if getattr(settings, 'API_LOGGER_MODE'):
			ApiLogger.log(req_data={
				'app': app,
				'resource': resource,
				'method': method,
				'params': params,
				'req_instance': req
			}, resp_data={
				'resp_instance': resp
			}, mode=getattr(settings, 'API_LOGGER_MODE', None))

	def on_get(self, req, resp, app, resource):
		self.__call_api('get', app, resource, req, resp)

	def on_post(self, req, resp, app, resource):
		_method = req.params.get('_method', 'post')
		self.__call_api(_method, app, resource, req, resp)

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

def __load_error_handlers():
	"""
	加载错误处理器
	"""
	handlers = []
	if not getattr(settings, 'ERROR_HANDLERS', None):
		return handlers
	for handler in settings.ERROR_HANDLERS:
		items = handler.split('.')
		module_path = '.'.join(items[:-1])
		module_name = items[-1]
		module = __import__(module_path, {}, {}, ['*', ])
		klass = getattr(module, module_name, None)
		if klass:
			print ('load error handler {}'.format(handler))
			handlers.append(klass)
		else:
			print ('[ERROR]: invalid error handler {}'.format(handler))
	return handlers

def __load_domain_events(events):
	"""
	加载领域事件
	"""
	for event_name, modules in events.items():
		for module_name in modules:
			__import__(module_name, {}, {}, ['*',])
			print ('load domain event handler: {}'.format(module_name))

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
		pass

def create_app():
	load_resources()

	middlewares = __load_middlewares()
	falcon_app = falcon.API(middleware=middlewares)

	# 解析值为空的参数
	falcon_app.req_options.keep_blank_qs_values = True

	# 解析formdata
	falcon_app.req_options.auto_parse_form_urlencoded = True

	# 注册到Falcon
	falcon_app.add_route('/{app}/{resource}/', FalconResource())

	#加载错误处理器
	error_handlers = __load_error_handlers()
	for handler in error_handlers:
		falcon_app.add_error_handler(handler)

	# 加载领域事件处理器
	if hasattr(settings, 'DOMAIN_EVENT_HANDLERS'):
		__load_domain_events(settings.DOMAIN_EVENT_HANDLERS)

	if settings.DEBUG or getattr(settings, 'ENABLE_CONSOLE', False):
		from rust.dev_resource import service_console_resource
		falcon_app.add_route('/console/', service_console_resource.ServiceConsoleResource())

		from rust.dev_resource import static_resource
		falcon_app.add_sink(static_resource.serve_static_resource, '/static/')

	return falcon_app