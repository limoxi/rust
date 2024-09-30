# coding: utf-8

import sys

from rust.utils import autoreload
from rust.command.base_command import BaseCommand
from rust.core.exceptions import unicode_full_stack

DEFAULT_PORT = '9000'
DEFAULT_HOST = '127.0.0.1'

class Command(BaseCommand):
    """
    本地web服务
    """
    args = ''

    def handle(self, *args, **options):

        if len(args) == 1:
            self.addr = args[0]
            self.port = DEFAULT_PORT
        if len(args) == 2:
            self.addr = DEFAULT_HOST
            self.port = args[1]
        else:
            self.addr = DEFAULT_HOST
            self.port = DEFAULT_PORT
        self.stdout = sys.stdout
        self.run(*args, **options)

    def run(self, *args, **options):

        autoreload.main(self.inner_run, args, options)

    def inner_run(self, *args, **options):
        self.stdout.write('\n>>>>>>>>>>>local server started @{}:{}<<<<<<<<<<< \n'.format(
            self.addr,
            self.port
        ))

        try:
            from wsgiref import simple_server
            from rust import apps
            wsgi_application = apps.create_app()

            httpd = simple_server.make_server(self.addr, int(self.port), wsgi_application)
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print (unicode_full_stack())