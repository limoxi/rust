#coding: utf8

from rust.core import business
from rust.resources.business.permission.permission_group_repository import PermissionGroupRepository

class FillService(business.Service):

	def fill(self, users, with_options):
		if with_options.get('with_group_info'):
			self.fill_group_info(users)

	def fill_group_info(self, users):
		"""
		填充分组信息
		"""
		user_ids = [u.id for u in users]
		user_id2group = PermissionGroupRepository().get_user_id2group(user_ids)
		for user in users:
			group = user_id2group.get(user.id)
			user.group = group