#coding: utf8

import os

#信息输出配置
API_LOGGER_MODE = 'ALL'
ENABLE_CONSOLE = (os.environ.get('_ENABLE_API_CONSOLE', '1') == '1')

#无需经过中间件的资源
DIRECT_PATHS = [
    '/static',
    '/console',
    '/logined_user',
    '/registered_user',
    '/groups',
]

RUST_RESOURCES = [
    'test',
    'user',
    'permission',
]

CORS_WHITE_LIST = [] #为空则表示接受所有host