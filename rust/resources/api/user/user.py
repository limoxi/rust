
from rust.core.business import ParamObject
from rust.core.api import ApiResource, Resource
from rust import Config
from rust.core.decorator import param_required
from rust.core.exceptions import BusinessError
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.fill_service import FillService

from rust.resources.business.user.user_factory import UserFactory
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

from rust.resources.business.user.user_repository import UserRepository

@Resource('rust.user.user')
class User(ApiResource):
	"""
	用户
	"""
	resource = 'rust.user.user'

	@param_required(['user', 'user_id:int', '?with_options:json'])
	def get(self):
		target_user = UserRepository().get_by_id(self.params['user_id'])
		with_options = self.params.get('with_options')
		if with_options:
			FillService().fill([target_user], with_options)
		return EncodeService().encode(target_user, with_options)

	@param_required(['user', 'username', '?group_id:int'])
	def put(self):
		"""
		创建用户只能由管理员操作，且只能初始化登录名和分组(角色)
		"""
		if not self.params['user'].is_manager:
			raise BusinessError(u'操作无权限')
		param_object = ParamObject({
			'username': self.params['username'],
			'password': Config.get_str('default_auth_password', '123456')
		})
		user = UserFactory().create(param_object)
		if self.params.get('group_id'):
			group = PermissionGroupRepository().get_by_id(self.params['group_id'])
			if group:
				group.add_user(user)
		return {
			'id': user.id
		}

	@param_required(['user', '?nickname', '?avatar', '?group_id:int'])
	def post(self):
		param_object = ParamObject({
			'nickname': self.params.get('nickname'),
			'password': self.params.get('password'),
			'avatar': self.params.get('avatar')
		})
		UserFactory(self.params['user']).update(param_object)
		if self.params.get('group_id'):
			group = PermissionGroupRepository().get_by_id(self.params['group_id'])
			if group:
				group.add_user(self.params['user'])
		return {}