from setuptools import setup, find_packages

version = __import__('rust').get_version()

def collect_requires():
	try:
		with open('requirements.txt', 'r') as f:
			contents = f.readlines()
		return map(lambda content: content.strip(), contents)
	except Exception as e:
		print('there is no requirements.txt', e)
		return ['click', 'falcon','werkzeug']

setup(
	name='rust',
	version=version,
	url='https://github.com/limoxi/rust.git',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=find_packages(),
	install_requires=collect_requires(),
	python_requires='>=3.6',
	classifiers=[
        'Programming Language :: Python :: 3'
    ],
	entry_points='''
		[console_scripts]
		rust-cli=rust.utils.rust_cli:cli
	''',
)