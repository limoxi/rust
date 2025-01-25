
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required

from rust.resources.business.permission.permission_repository import PermissionRepository
from rust.resources.business.permission.permission_service import PermissionService

@Resource('rust.permission.user_limited_permissions')
class UserLimitedPermissions(ApiResource):

	@param_required(['user', 'limited_user_id'])
	def get(self):
		user = self.params['user']
		permissions = PermissionRepository(user).get_user_limited_permissions(
			self.params['limited_user_id']
		)

		return [{
			'id': permission.id,
			'resource': permission.resource,
			'method': permission.method
		} for permission in permissions]

	@param_required(['user', 'limited_user_id:int', 'permission_ids:json'])
	def post(self):
		user = self.params['user']
		PermissionService(user).limit_user_permissions(
			self.params['limited_user_id'], self.params['permission_ids']
		)
		return {}