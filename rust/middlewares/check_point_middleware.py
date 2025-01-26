from rust import Config
from rust.core.middleware import BaseMiddleware

class CheckPointMiddleware(BaseMiddleware):
	def process_request(sel, req, resp):
		"""
		检查是否需要经由中间价
		"""
		if len(list(filter(lambda path: path in req.path, Config.get_list('rust.middleware.ignored_paths')))) > 0:
			req.context['__middleware_passed'] = True

		if req.method.upper() == 'OPTIONS':
			req.context['__middleware_passed'] = True

	def process_response(self, req, resp, resource, req_succeeded):
		"""
		实现CORS
		"""
		valid_host = '*'
		white_list = Config.get_list('rust.cors.white_list')
		if req.host in white_list:
			valid_host = req.host

		if valid_host:
			resp.set_header("Access-Control-Allow-Origin", valid_host)
			resp.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
			resp.set_header("Access-Control-Allow-Headers",
							"Origin, Authorization, X-Requested-With, Content-Type, Accept")

