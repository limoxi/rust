# -*- coding: utf-8 -*-

from rust.core.api_resource import ApiResource
from rust.core.decorator import param_required

from rust.resources.business.permission.permission_repository import PermissionRepository
from rust.resources.business.permission.permission_service import PermissionService

class AUserLimitedPermissions(ApiResource):

	app = 'rust.permission'
	resource = 'user_limited_permissions'

	@param_required(['user', 'limited_user_id'])
	def get(params):
		user = params['user']
		permissions = PermissionRepository(user).get_user_limited_permissions(params['limited_user_id'])

		return [{
			'id': permission.id,
			'resource': permission.resource,
			'method': permission.method
		} for permission in permissions]

	@param_required(['user', 'limited_user_id:int', 'permission_ids:json'])
	def post(params):
		user = params['user']
		PermissionService(user).limit_user_permissions(params['limited_user_id'], params['permission_ids'])
		return {}