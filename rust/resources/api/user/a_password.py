#coding: utf8

from rust.core.api import ApiResource
from rust.core.decorator import param_required
from rust.core.exceptions import BusinessError
from rust.resources.business.user.login_service import LoginService

class APassowrd(ApiResource):
	"""
	登录密码
	"""
	app = 'rust.user'
	resource = 'password'

	@param_required(['user', 'old_pwd', 'new_pwd'])
	def post(params):
		user = params['user']
		login_service = LoginService()
		if user.password != login_service.encrypt_password(params['old_pwd']):
			raise BusinessError(u'旧密码不正确')

		login_service.update_password(user, params['new_pwd'])

		return {}