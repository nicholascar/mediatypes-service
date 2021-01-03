import sys
import logging
from os.path import *

THIS_DIR = dirname(realpath(__file__))
sys.path.insert(0, THIS_DIR)
sys.path.insert(0, join(THIS_DIR, 'api'))
logging.basicConfig(stream=sys.stderr)

from app import app as application
