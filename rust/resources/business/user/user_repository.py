#coding: utf8

from datetime import datetime

from rust.core import business
from rust.core.exceptionutil import BusinessError

from rust.resources.business.user.user import User
from rust.resources.db.user import models as user_models

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
		db_model = user_models.User.select().dj_where(name=username).first()
		if db_model:
			return User(db_model)

	def get_by_session_key(self, session_key):
		now_time = datetime.now()
		db_model = user_models.UserSession.select().dj_where(session_key=session_key).first()
		if not db_model:
			raise BusinessError('invalid session_key')

		if db_model.expire_date < now_time:
			raise BusinessError('expired session_key')

		return self.get_by_id(db_model.user_id)

	def get_by_ids(self, user_ids):
		db_models = user_models.User.select().dj_where(id__in=user_ids)
		return [User(db_model) for db_model in db_models]