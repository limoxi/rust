
import json

from rust.core.exceptions import BusinessError

class MiddlewareException(BusinessError):

	@staticmethod
	def handle(req, resp, ex, params):
		resp.body = json.dumps({
			'code': 533,
			'errMsg': ex.get_message(),
		})