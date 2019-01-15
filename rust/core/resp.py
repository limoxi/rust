# -*- coding: utf-8 -*-

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

class SystemErrorResponse(ResponseBase):
	__slots__ = (
		'code',
		'errMsg',
		'innerErrMsg',
	)

	def __init__(self, code=500, errMsg='', innerErrMsg=''):
		self.code = code
		self.errMsg = errMsg
		self.innerErrMsg = innerErrMsg or errMsg

		super(SystemErrorResponse, self).__init__()

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
		'errMsg',
		'innerErrMsg',
	)

	def __init__(self, data):
		super(JsonResponse, self).__init__()
		self.code = 200
		self.data = {}
		self.errMsg = ''
		self.innerErrMsg = ''
		if type(data) == tuple:
			self.code = data[0]
			self.data = data[1]
			if self.code != 200:
				self.errMsg = self.data
				self.innerErrMsg = self.data

		self.body = data

	def to_string(self):
		return json.dumps({
			'code': self.code,
			'data': self.data,
			'errMsg': self.errMsg,
			'innerErrMsg': self.innerErrMsg
		})

class RawResponse(ResponseBase):

	def __init__(self, data):
		super(RawResponse, self).__init__()
		self.body = data

	def to_string(self):
		return self.body