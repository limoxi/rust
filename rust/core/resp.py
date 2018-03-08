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

	def __init__(self, data):
		super(JsonResponse, self).__init__()
		response = {
			'code': 200,
			'data': {},
			'errMsg': '',
			'innerErrMsg': ''
		}
		if type(data) == tuple:
			response['code'] = data[0]
			response['data'] = data[1]
			if response['code'] != 200:
				response['errMsg'] = response['data']
				response['innerErrMsg'] = response['data']
		else:
			response['code'] = 200
			response['data'] = data

		self.body = response

	def to_string(self):
		return json.dumps(self.body)

class RawResponse(ResponseBase):

	def __init__(self, data):
		super(RawResponse, self).__init__()
		self.body = data

	def to_string(self):
		return self.body