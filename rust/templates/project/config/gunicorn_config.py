# -*- coding: utf-8 -*-

import os
from multiprocessing import cpu_count

__SERVICE_HOST = os.environ.get('_SERVICE_HOST', '0.0.0.0')
__SERVICE_PORT = os.environ.get('_SERVICE_PORT', 9001)


__MODE = os.environ.get('_MODE', 'develop')

__is_dev = __MODE == 'develop'

reload = __is_dev
bind = '{}:{}'.format(__SERVICE_HOST, __SERVICE_PORT)
workers = 1 if __is_dev else cpu_count()

proc_name = '&service_name'

