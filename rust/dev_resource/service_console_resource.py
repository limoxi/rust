# -*- coding: utf-8 -*-
import os
import falcon

from rust.core import api_resource
from rust import RUST_PATH

from rust.apps import load_resources
load_resources()

class ServiceConsoleResource:
	"""
	返回service console页面
	"""
	def __init__(self):
		pass

	def on_get(self, req, resp):
		resources = [resource.replace('-', '.') for resource in api_resource.APPRESOURCE2CLASS.keys()]
		resources.sort()
		options = ['<option value="%s">%s</option>' % (resource, resource) for resource in resources]

		resp.content_type = 'text/html'
		resp.status = falcon.HTTP_200
		console_file_path = os.path.join(RUST_PATH, 'static/service_console.html')
		src = open(console_file_path)
		content = src.read()
		content = content.replace('{{ resources }}', '\n'.join(options))
		src.close()
		resp.body = content 