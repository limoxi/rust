from pathlib import Path
from setuptools import setup, find_packages

def collect_requires():
	try:
		with open(Path(__file__).parent / 'requirements.txt', encoding='utf-8') as f:
			contents = f.readlines()
		return list(map(lambda content: content.strip(), contents))
	except Exception as e:
		print('there is no requirements.txt', e)
		return ['click', 'falcon','werkzeug','ruamel.yaml']

setup(
	name='rust',
	version='1.0.0',
	url='https://github.com/limoxi/rust.git',
	author='aix',
	author_email='asia-aixiang@163.com',
	packages=find_packages(),
	install_requires=collect_requires(),
	python_requires='>=3.11',
	classifiers=[
        'Programming Language :: Python :: 3'
    ],
	entry_points='''
		[console_scripts]
		rust-cli=rust.utils.rust_cli:cli
	''',
)