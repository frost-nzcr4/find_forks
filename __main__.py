# coding: utf-8
"""Finds all forks of user/repo on github from the console."""
from __future__ import absolute_import, division, print_function, unicode_literals

from six import PY3

try:
    from .find_forks.find_forks import main
except (ImportError, SystemError) as ex:
    if PY3:
        from find_forks.find_forks import main
    else:
        raise
except ValueError as ex:
    if not PY3:
        from find_forks.find_forks import main
    else:
        raise

if __name__ == '__main__':
    main()
