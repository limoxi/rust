#coding: utf8

import click

@click.group()
def cli():
    pass

@click.command()
@click.argument('resource_name', required=True)
def add_resource(resource_name):
    click.echo('cli add ' + resource_name)

@click.command()
@click.argument('project_name', required=True)
def init_project(project_name):
    click.echo('cli create' + project_name)

@click.command()
def gen_requirements_file():
    import os
    os.system('pipreqs --force ./')
    click.echo('requirements.txt generated')

cli.add_command(add_resource) #增加资源
cli.add_command(init_project) #初始化新项目
cli.add_command(gen_requirements_file) #生成requirements.txt文件