#coding: utf8

from rust.core import business
from rust.core.decorator import cached_context_property

from rust.resources.business.permission.permission_repository import PermissionRepository

class User(business.Model):

	__slots__ = (
		'id',
		'username',
		'password',
		'nickname',
		'avatar',
		'is_manager',
		'created_at',
	)

	def __init__(self, db_model=None):
		super(User, self).__init__(db_model)

	@property
	def permissions(self):
		return PermissionRepository(self).get_user_permissions()

	@cached_context_property
	def group(self):
		return None