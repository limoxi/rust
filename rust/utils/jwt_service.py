# coding: utf-8

import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta

from rust.core.exceptions import BusinessError

import settings

SECRET = 'aSsJKgdAH2Dkaj1shd4ahsh' if not hasattr(settings, 'JWT_SECRET') else settings.JWT_SECRET
CURRENT_TOKEN = None

class JWTService(object):

	@staticmethod
	def get_current():
		return CURRENT_TOKEN

	@staticmethod
	def set_current(token):
		global CURRENT_TOKEN
		CURRENT_TOKEN = token

	def encode(self, data):
		ext_sec = 2*60*60 if not hasattr(settings, 'JWT_EXT_SEC') else settings.JWT_EXT_SEC
		payload = {
			'data': data,
			'exp': datetime.now() + timedelta(seconds=ext_sec)
		}
		return jwt.encode(payload, SECRET, algorithm='HS256')

	def decode(self, token):
		try:
			payload = jwt.decode(token, SECRET, algorithm='HS256')
		except InvalidTokenError:
			raise BusinessError(u'不合法的token')

		return payload['data']