# -*- coding: utf-8 -*-

from rust.core import api_resource

class ATest(api_resource.ApiResource):

	app = 'test'
	resource = 'test'

	def get(args):
		try:
			return {}
		except:
			return 500, 'error'