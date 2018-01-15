# -*- coding: utf-8 -*-

from rust.core.api_resource import ApiResource
from rust.core.decorator import param_required


class ATest(ApiResource):

	app = 'example'
	resource = 'test'

	@param_required(['id'])
	def get(params):
		print params


		return {
			'flag': 'success'
		}