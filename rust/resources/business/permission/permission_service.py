
from datetime import datetime

from rust.core import business

from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository
from rust.resources.business.permission.permission_repository import PermissionRepository
from rust.resources.db.permission import models as permission_models

class PermissionService(business.Service):

	def check_permission(self, resource, method):
		permission = PermissionRepository(self.user).get_by_resource_and_method(resource, method)
		if permission_models.UserLimitedPermission.select().dj_where(permission_id=permission.id).count() > 0:
			return False
		groups = PermissionGroupRepository(self.user).get_user_groups()
		group_ids = [g.id for g in groups]
		return permission_models.PermissionGroupHasPermission.select().dj_where(
			group_id__in=group_ids, permission_id=permission.id
		).count() > 0

	def limit_user_permissions(self, user_id, permission_ids):
		"""
		限制用户权限
		"""
		now_time = datetime.now()
		permission_models.UserLimitedPermission.delete().dj_where(user_id=user_id).execute()
		creation_list = [{
			'user_id': user_id,
			'permission_id': permission_id,
			'updated_at': now_time
		} for permission_id in permission_ids]

		len(creation_list) > 0 and permission_models.UserLimitedPermission.insert_many(creation_list).execute()