
class Model(object):
	"""
	领域业务对象的基类
	"""
	__slots__ = ('context', )

	def __init__(self, db_model=None):
		self.context = {}

		if db_model:
			self.context['db_model'] = db_model
			self._init_slot_from_model(db_model)
		else:
			for slot in self.__slots__:
				setattr(self, slot, None)

	def _init_slot_from_model(self, model, slots=None):
		if not slots:
			slots = self.__slots__

		for slot in slots:
			value = getattr(model, slot, None)
			if value != None:
				setattr(self, slot, value)
			else:
				setattr(self, slot, None)

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
	__slots__ = ('context', 'user', 'member')

	def __init__(self, user=None, member=None):
		self.context = {
			'user': user,
			'member': member
		}
		self.user = user
		self.member = member

def ParamObject(data):
	"""
	构建不可变属性对象
	"""
	class Inner(object):
		__slots__ = tuple(data.keys())

		def __init__(self, dict_data):
			for k, v in dict_data.items():
				setattr(self, k, v)

		def __getattr__(self, k):
			if k not in self.__slots__:
				return None
			return getattr(self, k)

	return Inner(data)