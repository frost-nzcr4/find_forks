#!/usr/bin/env python
# coding: utf-8
"""Run all tests."""
from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
import sys
import unittest

from six import PY3

if not PY3:
    try:
        from mock import __version__
    except ImportError:
        print('Please run `pip install mock`')
        raise


# Allow to run from console as ./tests/run.py
BASEPATH = path.abspath(path.join(path.dirname(__file__), '..'))
if BASEPATH not in sys.path:
    sys.path.append(BASEPATH)


def main():
    """Main function to run as shell script."""
    loader = unittest.TestLoader()
    suite = loader.discover(path.abspath(path.dirname(__file__)), pattern='test_*.py')
    runner = unittest.TextTestRunner(buffer=True)
    runner.run(suite)

if __name__ == '__main__':
    main()
