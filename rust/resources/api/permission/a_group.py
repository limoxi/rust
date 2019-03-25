# -*- coding: utf-8 -*-

from rust.core.business import ParamObject
from rust.core.api import ApiResource
from rust.core.decorator import param_required
from rust.resources.business.permission.permission_group_factory import PermissionGroupFactory

from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

class AGroup(ApiResource):

	app = 'rust.permission'
	resource = 'group'

	@param_required(['user', 'group_id', '?fill_permissions:bool'])
	def get(params):
		user = params['user']
		group = PermissionGroupRepository(user).get_by_id(params['group_id'])

		return {
			'id': group.id,
			'name': group.name,
			'desc': group.desc,
			'permissions': [{
				'id': permission.id,
				'name': permission.name,
				'desc': permission.desc
			} for permission in (group.permissions if params.get('fill_permissions') else [])]
		}

	@param_required(['user', 'name', '?desc'])
	def put(params):
		user = params['user']
		param_object = ParamObject({
			'name': params['name'],
			'desc': params.get('desc', '')
		})
		permission_group = PermissionGroupFactory(user).create(param_object)
		return {
			'group_id': permission_group.id
		}

	@param_required(['user', 'group_id', 'name', 'desc'])
	def post(params):
		user = params['user']
		param_object = ParamObject({
			'id': params['group_id'],
			'name': params['name'],
			'desc': params.get('desc', '')
		})
		PermissionGroupFactory(user).update(param_object)
		return {}

	@param_required(['user', 'group_id'])
	def delete(params):
		user = params['user']
		PermissionGroupFactory(user).delete(params['group_id'])
		return {}