
import json

from rust.core.exceptions import BusinessError

class MiddlewareException(BusinessError):

	@staticmethod
	def handle(req, resp, ex, params):
		resp.body = json.dumps({
			'code': 533,
			'errCode': 'request_failed',
			'errMsg': ex.get_message(),
		})