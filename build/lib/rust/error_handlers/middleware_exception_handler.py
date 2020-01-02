#coding: utf8

import json

from rust.core.exceptions import BusinessError

class MiddlewareException(BusinessError):

	@staticmethod
	def handle(ex, req, resp, params):
		resp.body = json.dumps({
			'code': 533,
			'errMsg': ex.get_message(),
			'innerErrMsg': ex.get_message()
		})