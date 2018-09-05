# -*- coding: utf-8 -*-

import os
import inspect
from rust.core.db import db

from rust.command.base_command import BaseCommand
from rust.core.exceptions import unicode_full_stack
from rust.core import db as models

DB_PATHS = [
	'db',
	'rust.resources.db'
]

class Command(BaseCommand):
	help = ""
	args = ''

	def handle(self, *args, **options):
		print ('syncdb: create table')
		db_models = []
		collected_tables = set()

		for path in DB_PATHS:
			module = __import__(path, {}, {}, ['*',])
			walk_path = os.path.dirname(os.path.abspath(module.__file__))
			for root, dirs, files in os.walk(walk_path):
				for f in files:
					if '__init__' in f:
						continue

					if f.endswith('.pyc'):
						continue

					if '.DS_Store' in f:
						continue

					upper_module = root.split(os.path.sep)[-1]
					module_name = '{}.{}.{}'.format(path, upper_module, f[:-3])
					print (module_name)
					try:
						module = __import__(module_name, {}, {}, ['*',])
						for key, value in module.__dict__.items():
							if inspect.isclass(value) and issubclass(value, models.Model) and value.__module__ == module.__name__:
								db_model = value
								table_name = db_model._meta.table_name
								if table_name in collected_tables:
									print ('[duplicate table]: ', table_name)
								else:
									print ('collect model: %s' % key)
									collected_tables.add(table_name)
									db_models.append(value)
					except:
						print (unicode_full_stack())

		print ('create {} tables, existed tables will not be created'.format(len(db_models)))
		try:
			db.create_tables(db_models)
		except:
			print unicode_full_stack()