# -*- coding: utf-8 -*-

from rust.core.api import ApiResource
from rust.core.decorator import param_required

from rust.resources.business.permission.permission_group_fill_service import PermissionGroupFillService
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

class AGroups(ApiResource):

	app = 'rust.permission'
	resource = 'groups'

	@param_required(['?user', '?fill_permissions:bool'])
	def get(params):
		user = params.get('user')
		groups = PermissionGroupRepository(user).get_groups()

		if params.get('fill_permissions', False) and user:
			PermissionGroupFillService(user).fill_permissions(groups)
		else:
			for group in groups:
				group.permissions = []

		return [{
			'id': group.id,
			'name': group.name,
			'desc': group.desc,
			'permissions': [{
				'id': permission.id,
				'resource': permission.resource,
				'method': permission.method
			} for permission in group.permissions]
		} for group in groups]