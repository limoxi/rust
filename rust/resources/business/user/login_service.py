#coding: utf8

import hashlib
import time
from datetime import datetime, timedelta

from rust.core import business
from rust.core.exceptions import BusinessError

from rust.resources.business.user.user_repository import UserRepository
from rust.resources.db.user import models as user_models

class LoginService(business.Service):

	def encrypt_password(self, raw_password):
		algorithm = 'sha1'
		salt = '69e44'
		hash = hashlib.sha1(salt + raw_password).hexdigest()
		return "%s$%s$%s" % (algorithm, salt, hash)

	def create_session(self, user):
		"""
		创建一次session
		"""
		today = datetime.now()
		session_key = 'member_{}_{}'.format(str(time.time()), user.id)
		session_key = hashlib.md5(session_key).hexdigest()

		user_models.UserSession.create(session_key=session_key, user_id=user.id, expire_date=today+timedelta(days=1))
		return session_key

	def login(self, username, raw_password):
		user = UserRepository().get_by_name(username)
		if not user:
			raise BusinessError('not exist')

		if user.password != self.encrypt_password(raw_password):
			raise BusinessError('incorrect password')

		return self.create_session(user)