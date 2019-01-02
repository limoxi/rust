# -*- coding: utf-8 -*-

import sys

from rust.core.exceptions import unicode_full_stack

def load_rust_command(command):
    module_name = 'rust.command.commands.%s' % command
    print ('load rust command: ', module_name)
    module = __import__(module_name, {}, {}, ['*',])
    return module

def load_local_command(command):
    module_name = 'commands.%s' % command
    print ('load local command: ', module_name)
    module = __import__(module_name, {}, {}, ['*',])
    return module

def run_command(command):
    try:
        command_module = load_rust_command(command)
    except:
        command_module = None
    if not command_module:
        command_module = load_local_command(command)

    if not command_module:
        print ('no command named: ', command)
    else:
        instance = getattr(command_module, 'Command')()
        try:
            instance.handle(*sys.argv[2:])
        except:
            print unicode_full_stack()