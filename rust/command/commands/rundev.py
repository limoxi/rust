import sys

from rust.command.base_command import BaseCommand
from rust.core.exceptions import print_full_stack
from werkzeug.serving import run_simple
from rust import apps

class Command(BaseCommand):
    """
    本地web服务, 用于开发
    """
    args = ''

    def handle(self, *args, **options):

        addr = '127.0.0.1'
        port = 9000

        if len(args) == 1:
            addr = args[0]
        if len(args) == 2:
            port = int(args[1])

        self.run(addr, port)

    def run(self, addr, port):
        sys.stdout.write('\n>>>>>>>>>>>local server started @{}:{}<<<<<<<<<<< \n'.format(
            addr,
            port
        ))

        try:
            app = apps.create_app()
            run_simple(addr, port, app, use_reloader=True)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print_full_stack()