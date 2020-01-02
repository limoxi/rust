# -*- coding: utf-8 -*-

from rust.error_handlers.middleware_exception_handler import MiddlewareException
from rust.resources.business.permission.permission_service import PermissionService
from rust.resources.business.user.user_repository import UserRepository
from rust.core.middleware import BaseMiddleware

class PermissionMiddleware(BaseMiddleware):
	def process_request(sel, req, resp):
		"""
		权限检查
		依赖user
		"""
		if req.context.get('__middleware_passed', False):
			return

		user = UserRepository.get()
		if user:
			if 'rust.permission' in req.path and user.name != 'manager':
				raise MiddlewareException(u'只有系统管理员才能管理权限')

			resource = req.context['_resource']
			method = req.context['_method']
			if not PermissionService(user).check_permission(resource, method):
				raise MiddlewareException(u'当前用户没有权限进行此操作')
		else:
			raise MiddlewareException(u'帐号不存在')

	def process_response(self, request, response, resource):
		pass