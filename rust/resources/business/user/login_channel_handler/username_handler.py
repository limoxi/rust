
import hashlib

from rust.core.business import ParamObject
from rust.resources.business.user.profile_params import ProfileParams

from rust.resources.business.user.user import User
from rust.resources.business.user.user_factory import UserFactory

from rust.core import business
from rust.core.exceptions import BusinessError
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.login_channel_handler import LoginChannelHandler
from rust.resources.business.user.user_repository import UserRepository
from rust.utils.jwt_service import JWTService

from rust.resources.db import user_models

@LoginChannelHandler('username')
class UsernameHandler(business.Service):

	def get_channel_name(self):
		return 'username'

	def update_password(self, user, new_pwd):
		encoded_pwd = self.encrypt_password(new_pwd)
		user_models.User.update(
			password = encoded_pwd
		).dj_where(id=user.id).execute()

	def encrypt_password(self, raw_password):
		algorithm = 'sha1'
		salt = '69e44'
		hash = hashlib.sha1(salt + raw_password).hexdigest()
		return "%s$%s$%s" % (algorithm, salt, hash)

	def check_username(self, username):
		return True

	def check_pwd(self, pwd):
		return True

	def register(self, register_params):
		if self.check_username(register_params.KEY) and self.check_pwd(register_params.SECRET):
			params = ParamObject({
				'name': register_params.NAME,
				'avatar': register_params.AVATAR,
			})
			user = User.create(params)

			profile_params = ProfileParams()
			profile_params.CHANNEL = self.get_channel_name()
			profile_params.KEY = register_params.KEY
			profile_params.SECRET = register_params.SECRET
			user.add_profile(profile_params)
			return user

	def login(self, login_params):
		user = UserRepository().get_by_name(login_params.KEY)
		if not user:
			raise BusinessError(u'用户不存在')

		if user.password != self.encrypt_password(login_params.SECRET):
			raise BusinessError(u'密码错误')

		return user