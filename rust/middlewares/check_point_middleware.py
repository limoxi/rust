
from rust.core.middleware import BaseMiddleware

import settings

class CheckPointMiddleware(BaseMiddleware):
	def process_request(sel, req, resp):
		"""
		检查是否需要经由中间价
		"""
		if len(filter(lambda path: path in req.path, settings.DIRECT_PATHS)) > 0:
			req.context['__middleware_passed'] = True

		if req.method.upper() == 'OPTIONS':
			req.context['__middleware_passed'] = True

	def process_response(self, req, resp, resource):
		"""
		实现CORS
		"""
		ANY_HOST = '*'
		if hasattr(settings, 'CORS_WHITE_LIST'):
			valid_host = ''
			if len(settings.CORS_WHITE_LIST) == 0:
				valid_host = ANY_HOST
			elif req.host in settings.CORS_WHITE_LIST:
				valid_host = req.host

			if valid_host:
				resp.set_header("Access-Control-Allow-Origin", valid_host)
				resp.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
				resp.set_header("Access-Control-Allow-Headers",
								"Origin, Authorization, X-Requested-With, Content-Type, Accept")
