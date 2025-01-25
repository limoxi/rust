
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.core.exceptions import BusinessError
from rust.resources.business.user.login_service import LoginService

@Resource('rust.user.password')
class Passowrd(ApiResource):
	"""
	登录密码
	"""

	@param_required(['user', 'old_pwd', 'new_pwd'])
	def post(self):
		user = self.params['user']
		login_service = LoginService()
		if user.password != login_service.encrypt_password(self.params['old_pwd']):
			raise BusinessError(u'旧密码不正确')

		login_service.update_password(user, self.params['new_pwd'])

		return {}