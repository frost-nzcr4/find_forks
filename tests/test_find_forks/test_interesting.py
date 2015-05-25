# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from six import PY3

from find_forks.find_forks import add_forks
from find_forks.interesting import print_interesting_forks

if PY3:
    from unittest.mock import patch, MagicMock, Mock  # pylint: disable=no-name-in-module
else:
    from mock import patch, MagicMock, Mock


class InterestingTest(unittest.TestCase):
    def test_print_interesting_forks(self):
        print_interesting_forks(sort='my_rule', custom_sorting_rules={'my_rule': lambda x: x[3]})

        url = 'https://github.com/frost-nzcr4/find_forks'
        response_mock = MagicMock()
        if PY3:
            response_mock.status = 200
        else:
            response_mock.code = 200
        response_mock.read = Mock(return_value='''[
  {
    "id": 1,
    "name": "find_forks",
    "full_name": "frost-nzcr4/find_forks",
    "owner": {
      "login": "frost-nzcr4"
    },
    "private": false,
    "fork": true,
    "forks_url": "https://api.github.com/repos/frost-nzcr4/find_forks/forks",
    "branches_url": "https://api.github.com/repos/frost-nzcr4/find_forks/branches{/branch}",
    "tags_url": "https://api.github.com/repos/frost-nzcr4/find_forks/tags",
    "created_at": "2015-05-15T07:50:00Z",
    "updated_at": "2015-05-15T07:50:00Z",
    "pushed_at": "2015-05-15T07:50:00Z",
    "git_url": "git://github.com/frost-nzcr4/find_forks.git",
    "ssh_url": "git@github.com:frost-nzcr4/find_forks.git",
    "clone_url": "https://github.com/frost-nzcr4/find_forks.git",
    "svn_url": "https://github.com/frost-nzcr4/find_forks",
    "forks": 0,
    "forks_count": 1,
    "watchers": 0,
    "watchers_count": 2,
    "stargazers_count": 3,
    "open_issues": 0,
    "open_issues_count": 0,
    "has_issues": false,
    "has_wiki": false,
    "has_pages": false,
    "default_branch": "master"
  }
]'''.encode('utf-8'))
        if PY3:
            response_mock.getheader = Mock(return_value='<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2>; rel="next", '
                                           '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=3>; rel="last"')
        else:
            response_mock.info = Mock(return_value=(('link', '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2>; rel="next", '
                                                             '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=3>; rel="last"'), ))

        with patch('find_forks.find_forks.urllib.request.urlopen', return_value=response_mock) as urlopen_mock:
            with patch('find_forks.git_wrapper.subprocess.call', return_value=None):
                self.assertEqual(add_forks(url), 'https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2')
                urlopen_mock.assert_called_once_with(url, timeout=6)
                if PY3:
                    response_mock.status = 404
                else:
                    response_mock.code = 404
                self.assertIsNone(add_forks(url))

        print_interesting_forks()
