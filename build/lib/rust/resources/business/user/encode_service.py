#coding: utf8

from rust.core import business
from rust.resources.business.permission.permission_group_encode_service import PermissionGroupEncodeService


class EncodeService(business.Service):

	def encode(self, user, with_options=None):
		with_options = with_options or {}
		encoded_data = {
			'id': user.id,
			'username': user.username,
			'nickname': user.nickname,
			'avatar': user.avatar,
			'is_manager': user.is_manager,
			'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
		}
		if with_options.get('with_group_info'):
			encoded_data['group'] = PermissionGroupEncodeService().encode(user.group)
		return encoded_data