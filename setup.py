from distutils.core import setup
import os

def fullsplit(path, result=None):
	"""
	Split a pathname into components (the opposite of os.path.join)
	in a platform-neutral way.
	"""
	if result is None:
		result = []
	head, tail = os.path.split(path)
	if head == '':
		return [tail] + result
	if head == path:
		return result
	return fullsplit(head, [tail] + result)

def is_package(package_name):
	return True

packages, package_data = [], {}

root_dir = os.path.dirname(__file__)
if root_dir != '':
	os.chdir(root_dir)
eaglet_dir = 'eaglet'

for dirpath, dirnames, filenames in os.walk(eaglet_dir):
	# Ignore PEP 3147 cache dirs and those whose names start with '.'
	dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
	parts = fullsplit(dirpath)
	package_name = '.'.join(parts)
	if '__init__.py' in filenames and is_package(package_name):
		packages.append(package_name)
	elif filenames:
		relative_path = []
		while '.'.join(parts) not in packages:
			relative_path.append(parts.pop())
		relative_path.reverse()
		path = os.path.join(*relative_path)

print packages

version = __import__('eaglet').get_version()

setup(
	name='eaglet', 
	version=version,
	url='/Users/Asia/Desktop/workspace/eaglet',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=packages
)