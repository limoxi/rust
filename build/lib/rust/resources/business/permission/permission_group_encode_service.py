#coding: utf8

from rust.core import business

from rust.resources.business.permission.permission_repository import PermissionRepository

class PermissionGroupEncodeService(business.Service):

	def encode(self, group):
		if not group:
			return {}
		return {
			'id': group.id,
			'name': group.name,
			'desc': group.desc,
		}
