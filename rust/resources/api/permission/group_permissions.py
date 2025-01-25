
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required

from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

@Resource('rust.permission.group_permissions')
class GroupPermissions(ApiResource):

	@param_required(['user', 'group_id'])
	def get(self):
		user = self.params['user']
		group = PermissionGroupRepository(user).get_by_id(self.params['group_id'])

		return [{
			'id': permission.id,
			'resource': permission.resource,
			'method': permission.method
		} for permission in group.permissions]

	@param_required(['user', 'group_id', 'permission_ids:json'])
	def post(self):
		user = self.params['user']
		group = PermissionGroupRepository(user).get_by_id(self.params['group_id'])
		group.set_permissions(self.params['permission_ids'])
		return {}