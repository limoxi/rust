#coding: utf8

from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.resources.business.user.login_service import LoginService

@Resource('rust.user.logined_user')
class ALoginedUser(ApiResource):
	"""
	登录用户
	"""
	@param_required(['username', 'password'])
	def put(self):
		return LoginService().login(self.params['username'], self.params['password'])