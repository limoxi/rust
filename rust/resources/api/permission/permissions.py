
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.resources.business.permission.permission_repository import PermissionRepository

@Resource('rust.permission.permissions')
class Permissions(ApiResource):

	@param_required(['user'])
	def get(self):
		user = self.params['user']

		permissions = PermissionRepository(user).get_permissions()
		permission2methods = dict()
		for permission in permissions:
			permission2methods.setdefault(permission.resource, []).append(permission.method)

		return [{
			'resource': p.resource,
			'methods': permission2methods.get(p.resource, [])
		} for p in permissions]