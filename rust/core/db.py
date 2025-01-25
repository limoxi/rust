
import json
import datetime
import peewee
from playhouse.pool import PooledMySQLDatabase, PooledPostgresqlDatabase, PooledSqliteDatabase

from . import hack_peewee # 重要！！勿删！！！

db = None
def init_sqlite_pool(db_path_and_name, max_cnn=8, timeout=60):
	global db
	db = PooledSqliteDatabase(
		db_path_and_name,  # 数据库文件路径
		max_connections=max_cnn,  # 最大连接数
		stale_timeout=timeout  # 连接空闲超时时间（秒）
	)

def init_pool(engine, db_host, db_name, db_user, db_password, db_port, max_cnn=8, timeout=60):
	global db
	if engine == 'mysql':
		db = PooledMySQLDatabase(
			db_name,  # 数据库名
			user=db_user,  # 用户名
			password=db_password,  # 密码
			host=db_host,  # 主机地址
			port=db_port,  # 端口
			max_connections=max_cnn,  # 最大连接数
			stale_timeout=timeout  # 连接空闲超时时间（秒）
		)
	elif engine == 'postgresql':
		db = PooledPostgresqlDatabase(
			db_name,  # 数据库名
			user=db_user,  # 用户名
			password=db_password,  # 密码
			host=db_host,  # 主机地址
			port=db_port,  # 端口
			max_connections=8,  # 最大连接数
			stale_timeout=300  # 连接空闲超时时间（秒）
		)

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