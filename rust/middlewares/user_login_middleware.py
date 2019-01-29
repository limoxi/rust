# -*- coding: utf-8 -*-

from rust.core.exceptions import BusinessException
from rust.core.middleware import BaseMiddleware
from rust.error_handlers.middleware_exception_handler import MiddlewareException
from rust.resources.business.user.user_repository import UserRepository

import settings

class UserLoginMiddleware(BaseMiddleware):
	def process_request(sel, req, resp):
		"""
		检查用户登录状态
		请求header中的AUTHORIZATION需要带有正确的token
		token是在登录成功后，api返回给请求端的数据
		如果实在开发模式下，可以在请求中加入__dev_uid，表示user_id，即可无需加入token
		"""
		user = None
		UserRepository.set(user)

		if req.context.get('__middleware_passed', False):
			return

		token = req.headers.get('AUTHORIZATION')
		if not token and settings.MODE == 'develop':
			user_id = req.params.get('__dev_uid')
			user = UserRepository().get_by_id(user_id)

		if token:
			try:
				user = UserRepository().get_by_token(token)
			except BusinessException as e:
				raise MiddlewareException(e.message)

		if user:
			req.context['user'] = user
			UserRepository.set(user)
		else:
			raise MiddlewareException(u'帐号不存在')

	def process_response(self, request, response, resource):
		pass