
from rust.core import business
from rust.core.decorator import cached_context_property

from rust.resources.business.permission.permission_repository import PermissionRepository

from rust.resources.db import user_models

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

	@classmethod
	def create(cls, param_object):
		db_model = user_models.User.create(
			name=param_object.name,
			avatar=param_object.avatar or ''
		)
		return cls(db_model)

	def add_profile(self, profile_params):
		if user_models.UserLoginProfile.select().dj_where(
			user_id=self.id,
			channel=profile_params.CHANNEL,
		).exists():
			return

		user_models.UserLoginProfile.create(
			user_id = self.id,
			channel = profile_params.CHANNEL,
			login_key = profile_params.KEY,
			login_secret = profile_params.SECRET,
		)