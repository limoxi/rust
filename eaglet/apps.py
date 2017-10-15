# -*- coding: utf-8 -*-

import decimal
import json
from datetime import datetime, date

import falcon
import settings

from eaglet import wapi as wapi_resource
from eaglet.core import api_resource
from eaglet.core.exceptionutil import unicode_full_stack


class ThingsResource:
	def on_get(self, req, resp):
		"""Handles GET requests"""
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('\nTwo things awe me most, the starry sky '
					 'above me and the moral law within me.\n'
					 '\n'
					 '    ~ Immanuel Kant Robert lalala\n\n')

class ApiListerResource:
	def on_get(self, req, resp):
		"""
		列出API
		"""
		api_list = []
		for (app_resource, resource_cls) in api_resource.APPRESOURCE2CLASS.items():
			app, resource = app_resource.split('-')
			api_cls = resource_cls['cls']
			api_info = {
				'app': app,
				'resource': resource,
				'class_name': str(api_cls),
				'explain': api_cls.__doc__.strip(),
				'methods': filter(lambda method: hasattr(api_cls, method), ['get', 'post', 'put', 'delete']),
			}
			api_list.append(api_info)
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(api_list)
		return

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
			response['code'] = 531 #不要改动这个code，531是表明service内部发生异常的返回码
			response['errMsg'] = str(e).strip()
			response['innerErrMsg'] = unicode_full_stack()

		resp.body = json.dumps(response, default=_default)

		if hasattr(settings, 'ACCESS_CONTROL_APP_PREFFIX'):
			if app.startswith(settings.ACCESS_CONTROL_APP_PREFFIX):
				resp.set_header("Access-Control-Allow-Origin", "*")
				resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

		if getattr(settings, 'DUMP_API_CALL_RESULT', True):
			# 记录RESOURCE_ACCESS日志
			resource_access_log = {}
			if getattr(settings, 'EAGLET_DISABLE_DUMP_REQ_PARAMS', False):
				resource_access_log['params'] = 'disabled by EAGLET_DISABLE_DUMP_REQ_PARAMS'
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

def create_app():
	#添加middleware
	middlewares = []
	for middleware in settings.MIDDLEWARES:
		items = middleware.split('.')
		module_path = '.'.join(items[:-1])
		module_name = items[-1]
		module = __import__(module_path, {}, {}, ['*',])
		klass = getattr(module, module_name, None)
		if klass:
			print 'load middleware %s' % middleware
			middlewares.append(klass())
		else:
			print '[ERROR]: invalid middleware %s' % middleware

	falcon_app = falcon.API(middleware=middlewares)

	# 解析值为空的参数
	falcon_app.req_options.keep_blank_qs_values = True

	# 注册到Falcon
	falcon_app.add_route('/{app}/{resource}/', FalconResource())

	# things will handle all requests to the '/things' URL path
	# Resources are represented by long-lived class instances
	#falcon_app.add_route('/things', ThingsResource())

	return falcon_app

