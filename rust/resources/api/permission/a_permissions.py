# -*- coding: utf-8 -*-

from rust.core.api import ApiResource
from rust.core.decorator import param_required
from rust.resources.business.permission.permission_repository import PermissionRepository

class APermissions(ApiResource):

	app = 'rust.permission'
	resource = 'permissions'

	@param_required(['user'])
	def get(params):
		user = params['user']

		permissions = PermissionRepository(user).get_permissions()
		permission2methods = dict()
		for permission in permissions:
			permission2methods.setdefault(permission.resource, []).append(permission.method)

		return [{
			'resource': p.resource,
			'methods': permission2methods.get(p.resource, [])
		} for p in permissions]