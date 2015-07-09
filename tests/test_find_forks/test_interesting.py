# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

from six import PY3

from find_forks.interesting import print_interesting_forks

from .test_find_forks import FindForksCommon

if PY3:
    from unittest.mock import patch, MagicMock, Mock  # pylint: disable=no-name-in-module
else:
    from mock import patch, MagicMock, Mock


class InterestingTest(FindForksCommon):
    def test_print_interesting_forks(self):
        print_interesting_forks(sort='my_rule', custom_sorting_rules={'my_rule': lambda x: x[3]})

        json_response = '''[
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
]'''.encode('utf-8')

        response_mock = self.make_mock(json_response)
        self.make_test(response_mock)

        print_interesting_forks()
