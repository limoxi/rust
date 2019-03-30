#coding: utf8

import re
import os
from string import Template

class RTemplate(Template):
	delimiter = '&'

TPL_DATA = dict()

def __create_file(path, inner_content):
	"""
	创建文件
	"""
	if not os.path.exists(path) or path.split(os.path.sep)[-1] == '__init__.py':
		with open(path, 'w') as f:
			f.write(inner_content)

def __create_files(src_path, target_path, file_names):
	for name in file_names:
		src_file_path = src_path + os.path.sep + name
		with open(src_file_path, 'r') as f:
			content_tmp = f.read()

		content = RTemplate(content_tmp).substitute(TPL_DATA)
		target_file_path = target_path + os.path.sep + name
		__create_file(target_file_path, content)

def __create_packages(pkg_path, pkgs):
	"""
	创建包
	"""
	for pkg in pkgs:
		full_path = '{}{}'.format(pkg_path, pkg)
		if not os.path.exists(full_path):
			os.makedirs(full_path)
			__create_file('{}{}__init__.py'.format(full_path, os.path.sep), '#coding: utf8')

def init_project(service_name):
	"""
	初始化项目
	"""
	global TPL_DATA
	TPL_DATA['service_name'] = service_name

	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_FILES_PATH = os.path.join(CURRENT_DIR, '..{sep}templates{sep}project'.format(
		sep = os.path.sep
	))
	target_relative_path = '.{sep}{service_name}{sep}'.format(
		sep = os.path.sep,
		service_name = service_name
	)
	for root, pkgs, pys in os.walk(TEMPLATE_FILES_PATH):
		sps = root.split(TEMPLATE_FILES_PATH)
		if len(sps) == 1:
			target_path = target_relative_path
			src_path = sps[0]
		else:
			target_path = '{rr}{sep}{tp}{sep}'.format(
				rr = target_relative_path,
				sep = os.path.sep,
				tp = sps[1]
			)
			src_path = root
		if pkgs:
			__create_packages(target_path, pkgs)

		if pys:
			__create_files(src_path, target_path, pys)

def add_resource(resource_name):
	"""
	增加资源
	"""
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	TEMPLATE_FILE_PATH = os.path.join(CURRENT_DIR, '..{sep}templates{sep}basic_resource_files.rtp'.format(
		sep = os.path.sep
	))
	with open(TEMPLATE_FILE_PATH, 'r') as f:
		content_tmp = f.read()

	content = Template(content_tmp).substitute({
		'resource_name': resource_name.encode('utf8'),
		'upper_resource_name': resource_name.title().encode('utf8')
	})

	groups = re.findall(r'(\S+)={16}\s{1}(\S*)\n(.*?)={16}end\n', content, re.DOTALL)

	for group in groups:
		type, path, inner_content = group
		if type == 'packages':
			__create_packages(path, inner_content.strip().split(','))
		elif type == 'addition':
			__addon_file_content(path, inner_content)
		else:
			__create_file(path, inner_content)

def __addon_file_content(path, inner_content):
	"""
	追加文件内容
	"""
	with open(path, 'a') as f:
		f.write(inner_content)

if __name__ == '__main__':
	init_project('test')
	add_resource('hell')