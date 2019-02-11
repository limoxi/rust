#coding: utf8

from rust.core.api import ApiResource
from rust.core.decorator import param_required
from rust.core.paginator import TargetPage
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.fill_service import FillService
from rust.resources.business.user.user_repository import UserRepository


class AUsers(ApiResource):
	"""
	用户列表
	"""
	app = 'rust.user'
	resource = 'users'

	@param_required(['user', '?page:int', '?count_per_page:int', '?filters:json', '?with_options:json'])
	def get(params):
		target_page = TargetPage(params)
		users = UserRepository().get_users(
			params.get('filters'),
			target_page
		)
		with_options = params.get('with_options')
		if with_options:
			FillService().fill(users, with_options)
		return {
			'users': [EncodeService().encode(user, with_options) for user in users],
			'page_info': target_page.to_dict() if target_page else {}
		}