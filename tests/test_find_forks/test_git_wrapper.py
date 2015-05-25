# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from six import PY3

from find_forks.git_wrapper import git_fetch_all, git_remote_add

if PY3:
    from unittest.mock import patch  # pylint: disable=no-name-in-module
else:
    from mock import patch


class GitWrapperTest(unittest.TestCase):
    def test_git_remote_add(self):
        name = 'frost-nzcr4'
        url = 'https://github.com/frost-nzcr4/find_forks.git'

        with patch('find_forks.git_wrapper.subprocess.call', return_value=None) as call_mock:
            git_remote_add(name, url)
        call_mock.assert_called_once_with(('git remote add %s %s' % (name, url)).split(' '))

    def test_git_fetch_all(self):
        with patch('find_forks.git_wrapper.subprocess.call', return_value=None) as call_mock:
            git_fetch_all()
        call_mock.assert_called_once_with(('git fetch --all').split(' '))
