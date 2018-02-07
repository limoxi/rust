#coding: utf8

from rust.core.api_resource import ApiResource
from rust.core.decorator import param_required
from rust.core.exceptionutil import BusinessError

from rust.resources.business.user.login_service import LoginService

ERROR_CODE2TEXT = {
	'not exist': u'用户不存在',
	'incorrect password': u'密码不正确',
}

class ALoginedUser(ApiResource):
	"""
	登录用户
	"""
	app = 'rust.user'
	resource = 'logined_user'

	@param_required(['name', 'password'])
	def put(params):
		try:
			session_key = LoginService().login(params['name'], params['password'])
			return {
				's_id': session_key
			}
		except BusinessError, e:
			return 500, e.get_message()