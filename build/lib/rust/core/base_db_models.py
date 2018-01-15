#coding: utf8

import peewee
from rust.core.hack_peewee import connect
import settings
import datetime

DB = settings.DATABASES['default']
db = None

if DB['NAME']:
	DB_URL = '%s://%s:%s@%s/%s' % (DB['ENGINE'], DB['USER'], DB['PASSWORD'],
		"%s:%s" % (DB['HOST'], DB['PORT']) if len(DB['PORT'])>0 else DB['HOST'], DB['NAME'])
	db = connect(DB_URL)
	db.connect()

class Model(peewee.Model):
	"""
	ORM基类
	"""
	class Meta:
		database = db

class IntegerField(peewee.IntegerField):

	def __init__(self, blank=False, db_index=False, **kwargs):
		kwargs['null'] = blank
		if db_index:
			kwargs['index'] = db_index
		super(IntegerField, self).__init__(**kwargs)


class CharField(peewee.CharField):

	def __init__(self, blank=False, db_index=False, **kwargs):
		kwargs['null'] = blank
		if db_index:
			kwargs['index'] = db_index
		super(CharField, self).__init__(**kwargs)


class TextField(peewee.TextField):
	pass

class BigIntegerField(peewee.BigIntegerField):
	pass

class FloatField(peewee.FloatField):
	pass

class DecimalField(peewee.DecimalField):
	pass

class DateTimeField(peewee.DateTimeField):

	def __init__(self, auto_now_add=False, auto_now=False, blank=False, **kwargs):
		if auto_now or auto_now_add:
			kwargs['default'] = datetime.datetime.now
		kwargs['null'] = blank
		super(DateTimeField, self).__init__(**kwargs)

class BooleanField(peewee.BooleanField):
	pass