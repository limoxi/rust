# coding: utf-8

import json

class ResponseBase(object):
	"""
	基类
	"""
	__slots__ = (
		'body',
	)

	def __init__(self):
		pass

	def to_string(self):
		raise NotImplementedError

class ErrorResponse(ResponseBase):
	__slots__ = (
		'code',
		'errMsg',
		'innerErrMsg',
	)

	@classmethod
	def get_from_exception(cls, e):
		instance = ErrorResponse(
			code = e.code,
			errMsg = e.message,
		)
		return instance

	def __init__(self, code=500, errMsg='', innerErrMsg=''):
		self.code = code
		self.errMsg = errMsg
		self.innerErrMsg = innerErrMsg or errMsg

		super(ErrorResponse, self).__init__()

	def to_string(self):
		return json.dumps({
			'code': self.code,
			'errMsg': self.errMsg,
			'innerErrMsg': self.innerErrMsg
		})

class JsonResponse(ResponseBase):

	__slots__ = (
		'code',
		'data',
	)

	def __init__(self, data):
		super(JsonResponse, self).__init__()
		self.code = 200
		self.data = data
		self.body = data

	def to_string(self):
		return json.dumps({
			'code': self.code,
			'data': self.data
		})

class RawResponse(ResponseBase):

	def __init__(self, data):
		super(RawResponse, self).__init__()
		self.body = data

	def to_string(self):
		return self.body