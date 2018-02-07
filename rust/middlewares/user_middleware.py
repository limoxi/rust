# -*- coding: utf-8 -*-

from rust.error_handlers.middlerware_exception_handler import MiddlewareException

from rust.resources.business.user.user_repository import UserRepository

import settings

ERROR_CODE2TEXT = {
	'invalid session_key': u'session不合法',
	'expired session_key': u'session已过期，请重新登录',
}

class UserMiddleware(object):
	def process_request(sel, req, resp):
		"""
		构建用户实例
		"""

		if len(filter(lambda path: path in req.path, settings.NO_NEED_LOGIN_PATHS)) > 0:
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