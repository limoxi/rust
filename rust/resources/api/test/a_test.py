# -*- coding: utf-8 -*-

from rust.core.api import ApiResource
from rust.core.decorator import param_required

class ATest(ApiResource):

	app = 'test'
	resource = 'test'

	@param_required(['id'])
	def get(params):

		return {
			'flag': 'success'
		}