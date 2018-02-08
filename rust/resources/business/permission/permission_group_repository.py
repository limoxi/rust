#coding: utf8

from rust.core import business

from rust.resources.business.permission.permission_group import PermissionGroup
from rust.resources.db.permission import models as permission_models

class PermissionGroupRepository(business.Service):

	def get_user_groups(self):
		relation_db_models = permission_models.PermissionGroupHasUser.select().dj_where(user_id=self.user.id)
		group_ids = [pgu.group_id for pgu in relation_db_models]
		return self.get_by_ids(group_ids)

	def get_by_id(self, group_id):
		db_model = permission_models.PermissionGroup.select().dj_where(id=group_id).first()
		if db_model:
			return PermissionGroup(db_model)

	def get_by_name(self, group_name):
		db_model = permission_models.PermissionGroup.select().dj_where(name=group_name).first()
		if db_model:
			return PermissionGroup(db_model)

	def get_by_ids(self, group_ids):
		db_models = permission_models.PermissionGroup.select().dj_where(id__in=group_ids)
		return [PermissionGroup(db_model) for db_model in db_models]

	def get_groups(self):
		db_models = permission_models.PermissionGroup.select()
		return [PermissionGroup(db_model) for db_model in db_models]