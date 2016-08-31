# coding: utf-8
"""Finds all forks of user/repo on github."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys


__version__ = '0.5.3'

logging.getLogger(__name__).addHandler(logging.NullHandler())

CONFIG = {
    'dry_run': False,
    'per_page': 100,  # Github limit answers to 100.
    'remote_name': 'origin',
    'start_page': 1
}
