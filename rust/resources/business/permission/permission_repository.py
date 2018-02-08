#coding: utf8

from rust.core import business

from rust.resources.business.permission.permission import Permission
from rust.resources.db.permission import models as permission_models

class PermissionRepository(business.Service):

	def get_by_resource_and_method(self, resource, method):
		db_model = permission_models.Permission.select().dj_where(
			resource_name = resource,
			method = method
		).first()

		if db_model:
			return Permission(db_model)

	def get_by_group(self, group_id):
		db_models = permission_models.PermissionGroupHasPermission.select().dj_where(group_id=group_id)
		permission_ids = [pgp.permission_id for pgp in db_models]
		return self.get_by_ids(permission_ids)

	def get_by_groups(self, group_ids, with_group=False):
		db_models = permission_models.PermissionGroupHasPermission.select().dj_where(group_id__in=group_ids)
		permission_ids = [pgp.permission_id for pgp in db_models]
		permissions = self.get_by_ids(permission_ids)
		if with_group:
			id2permission = {p.id: p for p in permissions}
			group2permission = dict()
			for db_model in db_models:
				group2permission.setdefault(db_model.group_id, []).append(id2permission[db_model.permission_id])
			return group2permission
		else:
			return permissions

	def get_by_ids(self, permission_ids):
		db_models = permission_models.Permission.select().dj_where(id__in=permission_ids)
		return [Permission(db_model) for db_model in db_models]

	def get_permissions(self):
		db_models = permission_models.Permission.select()
		return [Permission(db_model) for db_model in db_models]

	def get_user_permissions(self):
		user_id = self.user.id
		relation_db_models = permission_models.PermissionGroupHasUser.select().dj_where(user_id=user_id)
		group_ids = [pgu.group_id for pgu in relation_db_models]
		if len(group_ids) > 0:
			relation_db_models = permission_models.PermissionGroupHasPermission.select().dj_where(group_id__in=group_ids)
			permission_ids = [pgp.permission_id for pgp in relation_db_models]
		else:
			#没有分组则取所有权限
			permission_db_models = permission_models.Permission.select()
			permission_ids = [p.permission_id for p in permission_db_models]

		limited_permission_db_models = permission_models.UserLimitedPermission.select().dj_where(user_id=user_id)
		limited_permission_ids = [ulp.permission_id for ulp in limited_permission_db_models]
		valid_permission_ids = list(set(permission_ids) - set(limited_permission_ids))
		return self.get_by_ids(valid_permission_ids)

	def get_user_limited_permissions(self, user_id):
		relation_db_models = permission_models.UserLimitedPermission.select().dj_where(user_id=user_id)
		permission_ids = [ulp.permission_id for ulp in relation_db_models]
		return self.get_by_ids(permission_ids)