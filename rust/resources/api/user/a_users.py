#coding: utf8

from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required
from rust.core.paginator import TargetPage
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.fill_service import FillService
from rust.resources.business.user.user_repository import UserRepository

@Resource('rust.user.users')
class AUsers(ApiResource):
	"""
	用户列表
	"""

	@param_required(['user', '?page:int', '?count_per_page:int', '?filters:json', '?with_options:json'])
	def get(self):
		target_page = TargetPage(self.params)
		users = UserRepository().get_users(
			self.params.get('filters'),
			target_page
		)
		with_options = self.params.get('with_options')
		if with_options:
			FillService().fill(users, with_options)
		return {
			'users': [EncodeService().encode(user, with_options) for user in users],
			'page_info': target_page.to_dict() if target_page else {}
		}