
import os
import click

@click.group()
def cli():
    pass

@click.command()
@click.argument('resource_name', required=True)
def add(resource_name):
    os.system('python manage.py add_resource ' + resource_name)
    click.echo('resource added ' + resource_name)

@click.command()
@click.argument('project_name', required=True)
def init(project_name):
    click.echo('please be sure you have the rights to create files in current dir!')
    from rust_cli_func import init_project
    init_project(project_name)
    click.echo('project created ' + project_name)

@click.command()
def require():
    os.system('pipreqs --force ./')
    click.echo('requirements.txt generated')

cli.add_command(add) #增加资源
cli.add_command(init) #初始化新项目
cli.add_command(require) #生成requirements.txt文件