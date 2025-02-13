import sys
from rust.core.exceptions import print_full_stack
from wsgiref import simple_server
from rust import apps
import api  # don`t remove

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8123
    sys.stdout.write('\n>>>>>>>>>>>local server started @{}:{}<<<<<<<<<<< \n'.format(
        host,
        port
    ))
    try:
        app = apps.create_app()
        httpd = simple_server.make_server(host, port, app)
        print(f"Serving on http://{host}:{port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print_full_stack()