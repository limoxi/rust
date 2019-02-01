# -*- coding: utf-8 -*-

import os
__version__ = '0.3.3'

VERSION = __version__

RUST_PATH = os.path.dirname(os.path.abspath(__file__))

def get_version():
	return __version__
