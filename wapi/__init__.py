# -*- coding: utf-8 -*-

import time
import logging
from eaglet.core import api_resource

class ApiNotExistError(Exception):
	pass

def wapi_log(app, resource, method, data, time_start):
	logging.info('/{}/{}/{}?{} =====>{}'.format(app, resource, method, data, time.clock() - time_start))

def wapi_call(method, app, resource, data, req=None, resp=None):
	resource_name = resource
	key = '%s-%s' % (app, resource)
	start_at = time.clock()

	resource = api_resource.APPRESOURCE2CLASS.get(key, None)
	if not resource:
		wapi_log(app, resource_name, method, data, start_at)
		raise ApiNotExistError('%s:%s' % (key, method))

	func = getattr(resource['cls'], method, None)
	if not func:
		wapi_log(app, resource_name, method, data, start_at)
		raise ApiNotExistError('%s:%s' % (key, method))

	data['__req'] = req
	data['__resp'] = resp
	response = func(data)
	del data['__req']
	del data['__resp']
	wapi_log(app, resource_name, method, data, start_at)
	return response


def get(app, resource, data):
	return wapi_call('get', app, resource, data)


def post(app, resource, data):
	return wapi_call('post', app, resource, data)


def put(app, resource, data):
	return wapi_call('put', app, resource, data)


def delete(app, resource, data):
	return wapi_call('delete', app, resource, data)
