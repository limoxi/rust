# coding: utf-8

from rust.error_handlers.middleware_exception_handler import MiddlewareException
from rust.resources.business.user.user_repository import UserRepository
from rust.core.middleware import BaseMiddleware

class UserMiddleware(BaseMiddleware):
	def process_request(self, req, resp):
		"""
		构建用户实例
		"""
		if req.context.get('__middleware_passed', False):
			return

		user = UserRepository.get()
		if user:
			req.context['user'] = user
		else:
			user_id = req.params.get('user_id')
			if not user_id:
				user_id = req.params.get('__dev_uid')
				if not user_id:
					raise MiddlewareException(u'无用户信息, 请求不合法')

			user = UserRepository().get_by_id(user_id)

			if user:
				req.context['user'] = user
				UserRepository.set(user)
			else:
				raise MiddlewareException(u'帐号不存在')

	def process_response(self, request, response, resource):
		pass