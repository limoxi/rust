
import os
__version__ = '1.0.0'

VERSION = __version__

RUST_PATH = os.path.dirname(os.path.abspath(__file__))

def get_version():
	return __version__
