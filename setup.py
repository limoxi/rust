# coding: utf-8

import os
from setuptools import setup, find_packages

version = __import__('rust').get_version()

def find_extra_data(target_dirs):
	"""
	查找target_dir下所有目录和文件并组织成package_data要求的格式
	"""
	root_path = 'rust'
	root_path_ = root_path + '/'
	files = []
	for target_dir in target_dirs:
		static_path = root_path_ + target_dir

		def walk(_, dirname, names):
			for name in names:
				path = '{}/{}'.format(dirname, name)
				if os.path.isdir(path):
					os.path.walk(path, walk, None)
				elif os.path.isfile(path):
					files.append(path.replace(root_path_, ''))

		os.path.walk(static_path, walk, None)
	package_data = {root_path: files}
	print ('load console needed static files...')
	return package_data

def collect_requires():
	try:
		with open('requirements.txt', 'r') as f:
			contents = f.readlines()
		return map(lambda content: content.strip(), contents)
	except:
		return ['click']

setup(
	name='rust',
	version=version,
	url='https://github.com/limoxi/rust.git',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=find_packages(),
	package_data=find_extra_data(['static', 'templates']),
	install_requires=collect_requires(),
	entry_points='''
		[console_scripts]
		rust-cli=rust.utils.rust_cli:cli
	''',
)