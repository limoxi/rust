#coding: utf8

import hashlib

from rust.core import business
from rust.core.exceptions import BusinessError
from rust.resources.business.user.encode_service import EncodeService
from rust.resources.business.user.login_channel_handler import REGISTERED_HANDLERS
from rust.resources.business.user.user_repository import UserRepository
from rust.utils.jwt_service import JWTService

from rust.resources.db import user_models

class LoginService(business.Service):

	def __get_handler_by_channel(self, channel):
		handler = REGISTERED_HANDLERS.get(channel)
		if handler is None:
			raise BusinessError(u'暂不支持该方式')
		return handler

	def register(self, register_params):
		handler = self.__get_handler_by_channel(register_params.CHANNEL)
		user = handler.register(register_params)
		return user

	def login(self, login_params):
		handler = self.__get_handler_by_channel(login_params.CHANNEL)
		user = handler.login(login_params)

		encoded_user = EncodeService().encode(user)
		token = JWTService().encode(encoded_user)
		encoded_user['token'] = token
		return encoded_user