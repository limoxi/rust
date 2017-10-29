# -*- coding: utf-8 -*-

class Model(object):
	"""
	领域业务对象的基类
	"""
	__slots__ = ('context', )
	
	def __init__(self):
		self.context = {}

		for slot in self.__slots__:
			setattr(self, slot, None)

	def _init_slot_from_model(self, model, slots=None):
		if not slots:
			slots = self.__slots__

		for slot in slots:
			value = getattr(model, slot, None)
			if value != None:
				if 'id' == slot:
					value = int(value)
				setattr(self, slot, value)
			else:
				setattr(self, slot, None)

	def after_from_dict(self):
		"""
		from_dict调用结束前的hook函数，允许sub class修改from_dict的结果
		"""
		pass

	@classmethod
	def from_dict(cls, dict, slots=None):
		instance = cls()
		if not slots:
			slots = cls.__slots__

		for slot in slots:
			value = dict.get(slot, None)

			setattr(instance, slot, value)
		instance.after_from_dict()
		return instance

	def to_dict(self, *extras, **kwargs):
		result = dict()
		if kwargs and 'slots' in kwargs:
			slots = kwargs['slots']
		else:
			slots = self.__slots__

		for slot in slots:
			result[slot] = getattr(self, slot, None)

		if extras:
			for item in extras:
				result[item] = getattr(self, item, None)
			
		return result


class Service(object):
	"""
	领域服务的基类
	"""
	__slots__ = ('context', 'user' 'member')

	@classmethod
	def get(cls):

		return cls()
	
	def __init__(self, user=None, member=None):
		self.context = {
			'user': user,
			'member': member
		}
		self.user = user
		self.member = member

class Resource(object):
	"""
	交易中的资源
	"""
	__slots__ = (
		'context',
		'priority' #资源处理的优先级
	)

	def __init__(self):
		self.context = {}