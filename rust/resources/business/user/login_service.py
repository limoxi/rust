#coding: utf8

import hashlib

from rust.core import business
from rust.core.exceptions import BusinessException
from rust.resources.business.user.user_repository import UserRepository
from rust.utils.jwt_service import JWTService

class LoginService(business.Service):

	def encrypt_password(self, raw_password):
		algorithm = 'sha1'
		salt = '69e44'
		hash = hashlib.sha1(salt + raw_password).hexdigest()
		return "%s$%s$%s" % (algorithm, salt, hash)

	def login(self, username, raw_password):
		user = UserRepository().get_by_name(username)
		if not user:
			raise BusinessException('not exist', u'用户不存在')

		if user.password != self.encrypt_password(raw_password):
			raise BusinessException('incorrect password', u'密码错误')

		token = JWTService().encode({
			'id': user.id,
			'nickname': user.nickname,
			'avatar': user.avatar
		})

		return {
			'id': user.id,
			'nickname':  user.nickname,
			'avatar': user.avatar,
			'token': token
		}