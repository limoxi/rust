#coding: utf8

import hashlib

from rust.core import business
from rust.core.exceptions import BusinessError
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.user_repository import UserRepository
from rust.utils.jwt_service import JWTService

from rust.resources.db import user_models

class LoginService(business.Service):

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

	def login(self, username, raw_password):
		user = UserRepository().get_by_name(username)
		if not user:
			raise BusinessError(u'用户不存在')

		if user.password != self.encrypt_password(raw_password):
			raise BusinessError(u'密码错误')

		encoded_user = EncodeService().encode(user)
		token = JWTService().encode(encoded_user)
		encoded_user['token'] = token
		return encoded_user