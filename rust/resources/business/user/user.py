#coding: utf8

from rust.core import business

class User(business.Model):

	__slots__ = (
		'id',
		'name',
		'nick_name',
		'avatar',
		'role',
		'created_at',
	)

	def __init__(self, db_model):
		super(User, self).__init__()
		if db_model:
			self.context['db_model'] = db_model
			self._init_slot_from_model(db_model)