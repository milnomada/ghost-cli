import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')


from .client import GhostCli
from .tokener import Tokener
