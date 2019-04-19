#coding: utf8

from rust.core.business import ParamObject
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required

from rust.resources.business.user.user_factory import UserFactory
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

@Resource('rust.user.registered_user')
class ARegisteredUser(ApiResource):
	"""
	注册用户
	"""

	@param_required(['username', 'password', 'nickname', '?avatar', '?group_id:int'])
	def put(self):
		param_object = ParamObject({
			'username': self.params['username'],
			'password': self.params['password'],
			'nickname': self.params['nickname'],
			'avatar': self.params.get('avatar'),
		})
		user = UserFactory().create(param_object)
		if self.params.get('group_id'):
			group = PermissionGroupRepository().get_by_id(self.params['group_id'])
			if group:
				group.add_user(user)
		return {
			'id': user.id
		}
