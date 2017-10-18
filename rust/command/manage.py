# -*- coding: utf-8 -*-
import sys

def load_rust_command(command):
    module_name = 'rust.command.%s' % command
    print 'load rust command: ', module_name
    module = __import__(module_name, {}, {}, ['*',])
    return module

def load_local_command(command):
    module_name = 'commands.%s' % command
    print 'load local command: ', module_name
    module = __import__(module_name, {}, {}, ['*',])
    return module

def run_command(command):
    try:
        command_module = load_rust_command(command)
    except Exception as e:
        command_module = None
    if not command_module:
        command_module = load_local_command(command)

    if not command_module:
        print 'no command named: ', command
    else:
        instance = getattr(command_module, 'Command')()
        try:
            instance.handle(*sys.argv[2:])
        except TypeError, e:
            print '[ERROR]: wrong command arguments, usages:'
            print instance.help
            print 'Exception: {}'.format(e)