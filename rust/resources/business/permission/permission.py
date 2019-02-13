#coding: utf8

from rust.core import business

class Permission(business.Model):

	__slots__ = (
		'id',
		'resource',
		'method',
	)

	def __init__(self, db_model=None):
		super(Permission, self).__init__(db_model)