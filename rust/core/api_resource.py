# -*- coding: utf-8 -*-

APPRESOURCE2CLASS = dict()

class ApiResourceBase(type):
	def __new__(cls, name, bases, attrs):
		return super(ApiResourceBase, cls).__new__(cls, name, bases, attrs)

	def __init__(self, name, bases, attrs):
		if name == 'ApiResource':
			pass
		else:
			app_resource = '%s-%s' % (self.app, self.resource)

			for key, value in self.__dict__.items():
				if hasattr(value, '__call__'):
					static_method = staticmethod(value)
					setattr(self, key, static_method)

			APPRESOURCE2CLASS[app_resource] = {
				'cls': self,
				'instance': None
			}

		super(ApiResourceBase, self).__init__(name, bases, attrs)


class ApiResource(object):
	__metaclass__ = ApiResourceBase


def ParamObject(data):
	"""
	构建不可变属性对象
	"""
	class Inner(object):
		__slots__ = tuple(data.keys())

		def __init__(self, dict_data):
			for k, v in dict_data.items():
				setattr(self, k, v)

	return Inner(data)