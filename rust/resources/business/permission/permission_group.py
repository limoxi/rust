#coding: utf8

from rust.core.decorator import cached_context_property
from rust.core import business
from rust.core.base_db_models import db as peewee_db

from rust.resources.db.permission import models as permission_models

class PermissionGroup(business.Model):

	__slots__ = (
		'id',
		'name',
		'desc',
	)

	def __init__(self, db_model):
		super(PermissionGroup, self).__init__()
		if db_model:
			self.context['db_model'] = db_model
			self._init_slot_from_model(db_model)

	@cached_context_property
	def permissions(self):
		from rust.resources.business.permission.permission_repository import PermissionRepository
		return PermissionRepository().get_by_group(self.id)

	@peewee_db.atomic()
	def set_permissions(self, permission_ids):
		#首先删除之前的配置
		permission_models.PermissionGroupHasPermission.delete().dj_where(group_id=self.id).execute()
		creation_list = [{
			'group_id': self.id,
			'permission_id': permission_id
		} for permission_id in permission_ids]

		len(creation_list) > 0 and permission_models.PermissionGroupHasPermission.insert_many(creation_list).execute()