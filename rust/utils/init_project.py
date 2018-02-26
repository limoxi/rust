#coding: utf8

import re
import os
from string import Template

def init(service_name):
	"""
	初始化项目
	"""
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_FILE_PATH = os.path.join(CURRENT_DIR, '../templates/basic_project_files.rtp')
	with open(TEMPLATE_FILE_PATH, 'r') as f:
		content_tmp = f.read()

	content = Template(content_tmp).substitute({
		'service_name': service_name.encode('utf8')
	})

	groups = re.findall(r'(\S+)={16}\s{1}(\S*)\n(.*?)={16}end\n', content, re.DOTALL)

	for group in groups:
		type, path, inner_content = group
		if type == 'packages':
			__create_packages(path, inner_content)
		else:
			__create_file(path, inner_content)

def __create_packages(path, inner_content):
	"""
	创建包
	"""
	names = inner_content.strip().split(',')
	for dir_name in names:
		real_path = path+dir_name
		if not os.path.exists(real_path):
			os.mkdir(real_path)
			__create_file(real_path+'/__init__.py', '#coding: utf8')

def __create_file(path, inner_content):
	"""
	创建文件
	"""
	with open(path, 'w') as f:
		f.write(inner_content)