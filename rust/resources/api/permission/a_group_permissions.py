# -*- coding: utf-8 -*-

from rust.core.api import ApiResource
from rust.core.decorator import param_required

from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

class AGroupPermissions(ApiResource):

	app = 'rust.permission'
	resource = 'group_permissions'

	@param_required(['user', 'group_id'])
	def get(params):
		user = params['user']
		group = PermissionGroupRepository(user).get_by_id(params['group_id'])

		return [{
			'id': permission.id,
			'resource': permission.resource,
			'method': permission.method
		} for permission in group.permissions]

	@param_required(['user', 'group_id', 'permission_ids:json'])
	def post(params):
		user = params['user']
		group = PermissionGroupRepository(user).get_by_id(params['group_id'])
		group.set_permissions(params['permission_ids'])
		return {}