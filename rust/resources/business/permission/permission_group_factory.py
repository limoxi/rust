#coding: utf8

from rust.core.exceptions import BusinessError
from rust.core import business
from rust.core.db import db as peewee_db

from rust.resources.business.permission.permission_group import PermissionGroup
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository
from rust.resources.db.permission import models as permission_models

class PermissionGroupFactory(business.Service):

	def create(self, param_object):
		#重名检查
		name = param_object.name
		desc = param_object.desc
		if PermissionGroupRepository(self.user).get_by_name(name):
			raise BusinessError('existed')

		db_model = permission_models.PermissionGroup.create(
			name = name,
			desc = desc,
		)

		return PermissionGroup(db_model)

	def update(self, param_object):
		user = self.user
		group_id = param_object.id
		name = param_object.name
		desc = param_object.desc
		permission_group = PermissionGroupRepository(user).get_by_id(group_id)
		if not permission_group:
			raise BusinessError('not exist')

		if permission_group.name != name:
			permission_group.name = name

		if permission_group.desc != desc:
			permission_group.desc = desc

		permission_group.save()

	def delete(self, group_id):
		#首先删除用户数据
		permission_models.PermissionGroupHasUser.delete().dj_where(group_id=group_id).execute()
		#删除权限数据
		permission_models.PermissionGroupHasPermission.delete().dj_where(group_id=group_id).execute()
		#删除分组
		permission_models.PermissionGroup.delete().dj_where(group_id=group_id).execute()