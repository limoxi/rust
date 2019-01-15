#coding: utf8

from rust.core.api import ApiResource
from rust.core.decorator import param_required
from rust.resources.business.user.login_service import LoginService

class ALoginedUser(ApiResource):
	"""
	登录用户
	"""
	app = 'rust.user'
	resource = 'logined_user'

	@param_required(['username', 'password'])
	def put(params):
		return LoginService().login(params['username'], params['password'])