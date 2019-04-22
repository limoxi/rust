#coding: utf8

import os

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

DEBUG = (os.environ.get('_DEBUG', '0') == '1')
MODE = os.environ.get('_SERVICE_MODE', 'develop')
SERVICE_NAME = '&{service_name}'
SERVICE_HOST = '127.0.0.1'
SERVICE_PORT = 9001

UPLOAD_DIR = os.path.join(PROJECT_HOME, 'static', 'upload')  # 文件上传路径
UPLOAD_HTTP_PATH = '/static/upload'

def load_custom_configs():
    configs = {}
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
                    print '[WARN]: settings.%s(%s) is already defined' % (attr, f)

                configs[attr] = getattr(module, attr)

    return configs

locals().update(load_custom_configs())