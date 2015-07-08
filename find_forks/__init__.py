# coding: utf-8
"""Finds all forks of user/repo on github."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys


__version__ = '0.4.1'

logging.getLogger(__name__).addHandler(logging.NullHandler())

CONFIG = {
    'dry_run': False,
    'remote_name': 'origin'
}
