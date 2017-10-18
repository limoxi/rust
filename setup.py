
from setuptools import setup, find_packages

version = __import__('rust').get_version()

setup(
	name='rust',
	version=version,
	url='https://github.com/AsiaLi/rust.git',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=find_packages()
)