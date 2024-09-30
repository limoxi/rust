# coding: utf-8

import json
import urllib
import urlparse
import os
import requests
from time import time
import logging

from rust.core.exceptions import unicode_full_stack
from rust.utils.jwt_service import JWTService

CALL_SERVICE_WATCHDOG_TYPE = "USE_RESOURCE"
DEFAULT_TIMEOUT = 20
DEFAULT_GATEWAY_HOST = os.environ.get("API_GATEWAY", 'http://api.test.com')

def url_add_params(url, **params):
	""" 在网址中加入新参数 """
	pr = urlparse.urlparse(url)
	query = dict(urlparse.parse_qsl(pr.query))
	query.update(params)
	prlist = list(pr)
	prlist[4] = urllib.urlencode(query)
	return urlparse.ParseResult(*prlist).geturl()

class Inner(object):

	def __init__(self, service, gateway_host, config):
		self.service = service
		self.gateway_host = gateway_host
		self.__json_data = None
		self.api_scheme = config['api_scheme']
		self.__resource = ''
		if gateway_host.find('://') < 0:
			# 如果没有scheme，则自动补全
			self.gateway_host = "%s://%s" % (self.api_scheme, gateway_host)
		logging.info(u"gateway_host: {}".format(self.gateway_host))

		self.__resp = None
		self.access_token = None  # 暂时关闭

	def get(self, options):
		return self.__request(options['resource'], options['data'], 'get')

	def put(self, options):
		return self.__request(options['resource'], options['data'], 'put')

	def post(self, options):
		return self.__request(options['resource'], options['data'], 'post')

	def delete(self, options):
		return self.__request(options['resource'], options['data'], 'delete')

	def __request(self, resource, params, method):
		# 构造url
		"""
		@return is_success,code,data
		"""
		self.__resource = resource
		host = self.gateway_host

		resource_path = resource.replace('.', '/')

		service_name = self.service
		self.__target_service = service_name
		if service_name:
			base_url = '%s/%s/%s/' % (host, service_name, resource_path)
		else:
			# 如果resouce为None，则URL中省略resource。方便本地调试。
			base_url = '%s/%s/' % (host, resource_path)

		url = url_add_params(base_url)

		headers = {
			'AUTHORIZATION': JWTService.get_current()
		}

		start = time()
		try:
			# 访问资源
			if method == 'get':
				resp = requests.get(url, headers=headers, params=params, timeout=DEFAULT_TIMEOUT)
			elif method == 'post':
				resp = requests.post(url, headers=headers, data=params, timeout=DEFAULT_TIMEOUT)
			else:
				# 对于put、delete方法，变更为post方法，且querystring增加_method=put或_method=delete
				url = url_add_params(url, _method=method)
				resp = requests.post(url, headers=headers, data=params, timeout=DEFAULT_TIMEOUT)

			self.__resp = resp

			# 解析响应
			if resp.status_code == 200:

				json_data = json.loads(resp.text)
				self.__json_data = json_data
				code = json_data['code']

				if code == 200 or code == 500:
					self.__log(True, url, params, method)
					return json_data

				else:
					self.__log(False, url, params, method, 'ServiceProcessFailure', 'BUSINESS_CODE:' + str(code))
					return None
			else:
				self.__log(False, url, params, method, 'NginxError',
				           'HTTP_STATUS_CODE:' + str(resp.status_code))
				return None

		except requests.exceptions.RequestException as e:
			self.__log(False, url, params, method, str(type(e)), unicode_full_stack())
			return None
		except BaseException as e:
			self.__log(False, url, params, method, str(type(e)), unicode_full_stack())
			return None
		finally:
			stop = time()
			duration = stop - start
			logging.info('expend time {}'.format(duration))

	def __log(self, is_success, url, params, method, failure_type='', failure_msg=''):
		msg = {
			'url': url,
			'params': params,
			'method': method,
			'resource': self.__resource,
			'target_service': self.__target_service,
			'failure_type': failure_type,
			'failure_msg': failure_msg,
		}

		resp = self.__resp

		if resp:
			msg['http_code'] = resp.status_code
			if method == 'get' and is_success:
				msg['resp_text'] = 'stop_record'
			else:
				msg['resp_text'] = self.__json_data
		else:
			msg['http_code'] = ''
			msg['resp_text'] = ''

		print (msg)

class Resource(object):
	api_scheme = 'http'

	@classmethod
	def use(cls, service, gateway_host=DEFAULT_GATEWAY_HOST):
		return Inner(service, gateway_host, {
			'api_scheme': cls.api_scheme,
		})