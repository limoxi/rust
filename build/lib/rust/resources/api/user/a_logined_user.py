#coding: utf8

from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.resources.business.user.login_params import LoginParams
from rust.resources.business.user.login_service import LoginService

@Resource('rust.user.logined_user')
class ALoginedUser(ApiResource):
	"""
	登录用户
	"""
	@param_required(['login_key', 'login_secret', '?channel'])
	def put(self):
		params = LoginParams()
		params.KEY = self.params['login_key']
		params.SECRET = self.params['login_secret']
		params.CHANNEL = self.params.get('channel', 'username')
		return LoginService().login(params)