# coding: utf-8
"""Finds all forks of user/repo on github."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys


__version__ = '0.4.1'

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s %(name)s:%(lineno)d - %(message)s')

CONFIG = {
    'dry_run': False,
    'remote_name': 'origin'
}
