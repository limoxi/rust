#coding: utf8

from rust.core.business import ParamObject
from rust.core.api import ApiResource
from rust.core.decorator import param_required

from rust.resources.business.user.user_factory import UserFactory
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

class ARegisteredUser(ApiResource):
	"""
	注册用户
	"""
	app = 'rust.user'
	resource = 'registered_user'

	@param_required(['username', 'password', 'nickname', '?avatar', '?group_id:int'])
	def put(params):
		param_object = ParamObject({
			'username': params['username'],
			'password': params['password'],
			'nickname': params['nickname'],
			'avatar': params.get('avatar'),
		})
		user = UserFactory().create(param_object)
		if params.get('group_id'):
			group = PermissionGroupRepository().get_by_id(params['group_id'])
			if group:
				group.add_user(user)
		return {
			'id': user.id
		}
