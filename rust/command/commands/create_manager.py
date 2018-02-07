#coding: utf8

from rust.command.base_command import BaseCommand
from rust.resources.db.user import models as user_models
from rust.resources.business.user.login_service import LoginService

MANAGER_USER_NAME = 'manager'

class Command(BaseCommand):

	def handle(self, *args):
		"""
		创建系统管理员
		"""
		if user_models.User.select().dj_where(name=MANAGER_USER_NAME).count() == 0:
			user_models.User.create(
				name = MANAGER_USER_NAME,
				password = LoginService().encrypt_password('test')
			)

		#todo