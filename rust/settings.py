# -*- coding: utf-8 -*-

"""
project中新增settings，覆盖此文件
"""

import os

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

MODE = os.environ.get('_SERVICE_MODE', 'develop')
SERVICE_NAME = ''
DEV_SERVER_MULTITHREADING = False

DB_HOST = os.environ.get('_DB_HOST', 'db.dev.com')
DB_NAME = os.environ.get('_DB_NAME', 'emall')
DB_USER = os.environ.get('_DB_USER', 'peanut')
DB_PORT = os.environ.get('_DB_PORT', '3306')
DB_PASSWORD = os.environ.get('_DB_PASSWORD', 'njnarong')

DATABASES = {
    'default': {
        'ENGINE': 'mysql+retry',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': 100
    }
}

MIDDLEWARES = [
    'rust.middlewares.core_middleware.CoreMiddleware',

]

#请求输出配置
DUMP_API_CALL_RESULT = True

def load_custom_configs():
    configs = {}
    attr2file = {}
    for f in os.listdir('./config'):
        if f.startswith('__init'):
            continue

        if f.endswith('.py'):
            module_part = f[0:-3]
            module_name = 'config.{}'.format(module_part)
            module = __import__(module_name, {}, {}, ['*',])
            for attr in module.__dict__.keys():
                if attr.startswith('__'):
                    continue

                if attr in configs:
                    print '[WARN]: settings.%s(%s) is already defined in `%s`' % (attr, f, attr2file[attr])

                configs[attr] = getattr(module, attr)
                attr2file[attr] = f

    return configs            

locals().update(load_custom_configs())
