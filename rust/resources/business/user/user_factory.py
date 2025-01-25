
from rust.core import business
from rust.core.exceptions import BusinessError

from rust.resources.business.user.login_service import LoginService
from rust.resources.business.user.user import User
from rust.resources.db.user import models as user_models

class UserFactory(business.Service):

	def create(self, param_object):

		db_model = user_models.User.create(
			username = param_object.username,
			password = param_object.encrypted_password,
			nickname = param_object.nickname,
			avatar = param_object.avatar or ''
		)
		return User(db_model)

	def update(self, param_object):
		db_model = self.user.context['db_model']
		modified = False
		if param_object.nickname is not None and self.user.nickname != param_object.nickname:
			db_model.nickname = param_object.nickname
			modified = True

		if param_object.avatar is not None and self.user.avatar != param_object.avatar:
			db_model.avatar = param_object.avatar
			modified = True

		modified and db_model.save()