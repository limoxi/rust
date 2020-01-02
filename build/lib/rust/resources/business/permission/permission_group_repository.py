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

	def get_user_id2group(self, user_ids):
		db_models = permission_models.PermissionGroupHasUser.select().dj_where(
			user_id__in = user_ids
		)
		group_id2user_id = {db.group_id: db.user_id for db in db_models}
		db_models = permission_models.PermissionGroup.select().dj_where(
			id__in = group_id2user_id.keys()
		)
		id2group = {d.id: PermissionGroup(d) for d in db_models}
		user_id2group = dict()
		for id, group in id2group.items():
			user_id = group_id2user_id.get(id)
			if not user_id:
				continue
			user_id2group[user_id] = group

		return user_id2group
