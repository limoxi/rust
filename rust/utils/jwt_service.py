
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta

from rust import Config
from rust.core.exceptions import BusinessError

class JWTService(object):
	SECRET: str = Config.get_str('jwt.secret', 'aSsJKgdAH2Dkaj1shd4ahsh')
	EXPIRE_SECONDS: int = Config.get_int('jwt.expire_seconds', 2*60*60)

	def encode(self, data):
		payload = {
			'data': data,
			'exp': datetime.now() + timedelta(seconds=JWTService.EXPIRE_SECONDS)
		}
		return jwt.encode(payload, JWTService.SECRET, algorithm='HS256')

	def decode(self, token):
		try:
			payload = jwt.decode(token, JWTService.SECRET, algorithm='HS256')
		except InvalidTokenError:
			raise BusinessError(u'不合法的token')

		return payload['data']