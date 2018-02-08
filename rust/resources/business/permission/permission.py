#coding: utf8

from rust.core import business

class Permission(business.Model):

	__slots__ = (
		'id',
		'resource',
		'method',
	)

	def __init__(self, db_model):
		super(Permission, self).__init__()
		if db_model:
			self.context['db_model'] = db_model
			self._init_slot_from_model(db_model)