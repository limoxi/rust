#coding: utf8

import json
import datetime
import peewee
from playhouse.db_url import connect
import hack_peewee # 重要！！勿删！！！

try:
	import settings
except:
	raise RuntimeError('[start server failed]: a py file named settings in the project root dir needed !!!]')

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

	def __init__(self, db_index=False, **kwargs):
		if db_index:
			kwargs['index'] = db_index
		super(IntegerField, self).__init__(**kwargs)


class CharField(peewee.CharField):

	def __init__(self, db_index=False, **kwargs):
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

	def __init__(self, auto_now_add=False, **kwargs):
		if auto_now_add:
			kwargs['default'] = datetime.datetime.now
		super(DateTimeField, self).__init__(**kwargs)

class BooleanField(peewee.BooleanField):
	pass

class JsonField(peewee.TextField):

	def __init__(self, default=None, **kwargs):
		if default:
			kwargs['default'] = json.dumps(default)
		super(JsonField, self).__init__(**kwargs)

	def python_value(self, value):
		try:
			return json.loads(value)
		except:
			raise ValueError('data in db damaged !')

	def db_value(self, value):
		if type(value) != list:
			raise ValueError('invalid data type !')
		return json.dumps(value)

class ListField(JsonField):
	pass

class DictField(JsonField):
	pass