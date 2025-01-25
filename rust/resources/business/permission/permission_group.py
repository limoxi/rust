
from datetime import datetime

from rust.core.decorator import cached_context_property
from rust.core import business

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

	def set_permissions(self, permission_ids):
		#首先删除之前的配置
		permission_models.PermissionGroupHasPermission.delete().dj_where(group_id=self.id).execute()
		creation_list = [{
			'group_id': self.id,
			'permission_id': permission_id
		} for permission_id in permission_ids]

		len(creation_list) > 0 and permission_models.PermissionGroupHasPermission.insert_many(creation_list).execute()

	def add_user(self, user):
		"""
		user加入分组
		"""
		now = datetime.now()
		data = {
			'group_id': self.id,
			'user_id': user.id,
			'updated_at': now
		}
		if permission_models.PermissionGroupHasUser.select().dj_where(
				user_id = user.id
			).exists():
			permission_models.PermissionGroupHasUser.update(**data).dj_where(
				user_id=user.id
			).execute()
		else:
			permission_models.PermissionGroupHasUser.create(**data)