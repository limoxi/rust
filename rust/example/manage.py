#!/usr/bin/env python

import sys
from rust.command import command_manager

if __name__ == '__main__':
    command = sys.argv[1]
    command_manager.run_command(command)