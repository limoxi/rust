#coding: utf8

from rust.core import business
from rust.core.exceptions import BusinessError

from rust.resources.business.user.login_service import LoginService
from rust.resources.business.user.user import User
from rust.resources.db.user import models as user_models

class UserFactory(business.Service):

	def create(self, param_object):
		#检查重名
		if user_models.User.select().dj_where(name=param_object.name).count() > 0:
			raise BusinessError('existed')

		db_model = user_models.User.create(
			name = param_object.name,
			password = param_object.password
		)
		return User(db_model)

	def update(self, param_object):
		db_model = self.user.context['db_model']
		modified = False
		if param_object.nick_name is not None and self.user.nick_name == param_object.nick_name:
			db_model.nick_name = param_object.nick_name
			modified = True

		if param_object.password is not None:
			new_password = LoginService().encrypt_password(param_object.password)
			db_model.password = new_password
			modified = True

		if param_object.avatar is not None and self.user.avatar == param_object.avatar:
			db_model.avatar = param_object.avatar
			modified = True

		modified and db_model.save()