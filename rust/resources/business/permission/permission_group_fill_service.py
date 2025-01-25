
from rust.core import business

from rust.resources.business.permission.permission_repository import PermissionRepository

class PermissionGroupFillService(business.Service):

	def fill_permissions(self, groups):
		"""
		填充权限
		"""
		group_ids = [g.id for g in groups]
		group_id2permissions = PermissionRepository(self.user).get_by_groups(group_ids, with_group=True)
		for group in groups:
			group.permissions = group_id2permissions.get(group.id, [])