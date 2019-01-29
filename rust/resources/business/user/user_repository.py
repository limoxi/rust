#coding: utf8

from datetime import datetime

from rust.core import business
from rust.core.exceptions import BusinessError

from rust.resources.business.user.user import User
from rust.resources.db.user import models as user_models
from rust.utils.jwt_service import JWTService

CURRENT_USER = None

class UserRepository(business.Service):

	@classmethod
	def get(cls):
		global CURRENT_USER
		return CURRENT_USER

	@classmethod
	def set(cls, user):
		global CURRENT_USER
		CURRENT_USER = user

	def get_by_id(self, user_id):
		db_model = user_models.User.select().dj_where(id=user_id).first()
		if db_model:
			return User(db_model)

	def get_by_name(self, username):
		db_model = user_models.User.select().dj_where(username=username).first()
		if db_model:
			return User(db_model)

	def get_by_token(self, token):
		data = JWTService().decode(token)
		user_id = data['id']

		return self.get_by_id(user_id)

	def get_by_ids(self, user_ids):
		db_models = user_models.User.select().dj_where(id__in=user_ids)
		return [User(db_model) for db_model in db_models]