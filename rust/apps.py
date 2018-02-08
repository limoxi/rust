# -*- coding: utf-8 -*-

import decimal
import json
from datetime import datetime, date
import falcon

from rust import wapi as wapi_resource
from rust.core import api_resource
from rust.core.exceptionutil import unicode_full_stack

import api.resources

import settings

def _default(obj):
	if isinstance(obj, datetime): 
		return obj.strftime('%Y-%m-%d %H:%M:%S') 
	elif isinstance(obj, date): 
		return obj.strftime('%Y-%m-%d') 
	elif isinstance(obj, decimal.Decimal):
		return str(obj)
	else:
		raise TypeError('%r is not JSON serializable (type %s)' % (obj, type(obj)))

class FalconResource:
	def __init__(self):
		pass

	def call_wapi(self, method, app, resource, req, resp):
		req.context['_app'] = app
		req.context['_resource'] = resource
		response = {
			"code": 200,
			"errMsg": "",
			"innerErrMsg": "",
		}
		resp.status = falcon.HTTP_200
		
		args = {}
		args.update(req.params)
		args.update(req.context)
		args['wapi_id'] = req.path + '_' + req.method
		is_return_raw_data = False

		try:
			raw_response = wapi_resource.wapi_call(method, app, resource, args, req, resp)
			if type(raw_response) == tuple:
				response['code'] = raw_response[0]
				response['data'] = raw_response[1]
				if response['code'] != 200:
					response['errMsg'] = response['data']
					response['innerErrMsg'] = response['data']
			else:
				response['code'] = 200
				response['data'] = raw_response

			if response['code'] == 200:
				if type(response['data']) == dict and response['data'].get('__type') == 'raw':
					is_return_raw_data = True
					response = response['data'].get('data')
					if type(response) == dict:
						response['code'] = 200
					else:
						pass
					
		except wapi_resource.ApiNotExistError as e:
			response['code'] = 404
			response['errMsg'] = str(e).strip()
			response['innerErrMsg'] = unicode_full_stack()
		except Exception as e:
			response['code'] = 531 #内部异常
			response['errMsg'] = str(e).strip()
			response['innerErrMsg'] = unicode_full_stack()

		resp.body = json.dumps(response, default=_default)

		if getattr(settings, 'ACCESS_CONTROL_OPEN', False) and settings.ACCESS_CONTROL_OPEN:
			resp.set_header("Access-Control-Allow-Origin", "*")
			resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

		if getattr(settings, 'DUMP_API_CALL_RESULT', True):
			# 记录RESOURCE_ACCESS日志
			resource_access_log = {}
			if getattr(settings, 'RUST_DISABLE_DUMP_REQ_PARAMS', False):
				resource_access_log['params'] = 'disabled by RUST_DISABLE_DUMP_REQ_PARAMS'
			else:
				resource_access_log['params'] = req.params

			resource_access_log['app'] = app
			resource_access_log['resource'] = resource
			resource_access_log['method'] = method
			if method == 'get':
				resource_access_log['response'] = {
					'code': response['code'] if not is_return_raw_data else '__raw_data',
					'data': 'stop_record'
				}
			else:
				resource_access_log['response'] = json.loads(resp.body)

	def on_get(self, req, resp, app, resource):
		self.call_wapi('get', app, resource, req, resp)

	def on_post(self, req, resp, app, resource):
		_method = req.params.get('_method', 'post')
		self.call_wapi(_method, app, resource, req, resp)

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
			print 'load middleware %s' % middleware
			middlewares.append(klass())
		else:
			print '[ERROR]: invalid middleware %s' % middleware
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
			print 'load error handler %s' % handler
			handlers.append(klass)
		else:
			print '[ERROR]: invalid error handler %s' % handler
	return handlers

def __load_domain_events(events):
	"""
	加载领域事件
	"""
	for event_name, modules in events.items():
		for module_name in modules:
			__import__(module_name, {}, {}, ['*',])
			print 'load domain event handler: {}'.format(module_name)

def load_rust_resources():
	"""
	加载rust自带资源
	"""
	if hasattr(settings, 'RUST_RESOURCES'):
		for resource in settings.RUST_RESOURCES:
			__import__('rust.resources.api.{}'.format(resource), {}, {}, ['*', ])
			print 'load rust built-in resource: {}'.format(resource)

def create_app():
	load_rust_resources()

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