#coding: utf8

from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.resources.business.user.register_params import RegisterParams
from rust.resources.business.user.login_service import LoginService

@Resource('rust.user.registered_user')
class ARegisteredUser(ApiResource):
	"""
	注册用户
	"""
	@param_required(['login_key', 'login_secret', 'name', '?avatar', '?channel'])
	def put(self):
		params = RegisterParams()
		params.KEY = self.params['login_key']
		params.SECRET = self.params['login_secret']
		params.CHANNEL = self.params.get('channel', 'username')
		params.NAME = self.params['name']
		params.AVATAR = self.params.get('avatar', '')
		user = LoginService().register(params)
		return {
			'id': user.id
		}