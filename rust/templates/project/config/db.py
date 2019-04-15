#coding: utf8

import os

DB_HOST = os.environ.get('_DB_HOST', 'db.dev.com')
DB_NAME = os.environ.get('_DB_NAME', '&service_name')
DB_USER = os.environ.get('_DB_USER', '&service_name')
DB_PORT = os.environ.get('_DB_PORT', '3306')
DB_PASSWORD = os.environ.get('_DB_PASSWORD', '123456')

DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}