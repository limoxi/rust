# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = __import__('rust').get_version()

def find_extra_data(target_dir):
	"""
	查找target_dir下所有目录和文件并组织成package_data要求的格式
	"""
	root_path = 'rust'
	root_path_ = root_path + '/'
	static_path = root_path_ + target_dir
	files = []

	def walk(_, dirname, names):
		for name in names:
			path = '{}/{}'.format(dirname, name)
			if os.path.isdir(path):
				os.path.walk(path, walk, None)
			elif os.path.isfile(path):
				files.append(path.replace(root_path_, ''))

	os.path.walk(static_path, walk, None)
	package_data = {root_path: files}
	print 'load console needed static files...'
	print files
	return package_data

setup(
	name='rust',
	version=version,
	url='https://github.com/AsiaLi/rust.git',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=find_packages(),
	package_data=find_extra_data('static')
)