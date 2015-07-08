# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

import textwrap
import unittest

from six import PY3

from find_forks.__init__ import CONFIG
from find_forks.find_forks import add_forks, determine_names, find_forks, main

if PY3:
    from unittest.mock import patch, MagicMock, Mock  # pylint: disable=no-name-in-module
else:
    from mock import patch, MagicMock, Mock


class FindForksTest(unittest.TestCase):
    def test_add_forks(self):
        self.assertIsNone(add_forks('httttps://unavailable!url'))

        url = 'https://github.com/frost-nzcr4/find_forks'
        response_mock = MagicMock()
        if PY3:
            response_mock.status = 200
        else:
            response_mock.code = 200
        response_mock.read = Mock(return_value=textwrap.dedent('''
            [
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
                    "forks_count": 0,
                    "watchers": 0,
                    "watchers_count": 0,
                    "stargazers_count": 0,
                    "open_issues": 0,
                    "open_issues_count": 0,
                    "has_issues": false,
                    "has_wiki": false,
                    "has_pages": false,
                    "default_branch": "master"
                }
            ]''').encode('utf-8'))
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

    def test_determine_names(self):
        """To run this test you'll need to prepare git first, run:

        git remote add test-origin-1 https://github.com/frost-nzcr4/find_forks.git
        git remote add test-origin-2 https://github.com/yagmort/symfony1.git
        git remote add test-origin-3 git@github.com:tjerkw/Android-SlideExpandableListView.git
        """
        user, repo = determine_names()
        self.assertEqual(user, 'frost-nzcr4')
        self.assertEqual(repo, 'find_forks')

        user, repo = determine_names('test-origin-1')
        self.assertEqual(user, 'frost-nzcr4')
        self.assertEqual(repo, 'webmoney')

        user, repo = determine_names('test-origin-2')
        self.assertEqual(user, 'yagmort')
        self.assertEqual(repo, 'symfony1')

        user, repo = determine_names('test-origin-3')
        self.assertEqual(user, 'tjerkw')
        self.assertEqual(repo, 'Android-SlideExpandableListView')

        with self.assertRaises(RuntimeError):
            user, repo = determine_names('name-with-an-error')

    def test_find_forks(self):
        sent_args = {
            'per_page': 99,
            'start_page': 3
        }
        url = 'https://api.github.com/repos/frost-nzcr4/find_forks/forks?per_page=%s&page=%s' % (sent_args['per_page'], sent_args['start_page'])

        with patch('find_forks.git_wrapper.subprocess.call', return_value=None) as call_mock:
            with patch('find_forks.find_forks.add_forks', return_value=None) as add_forks_mock:
                find_forks(**sent_args)
        add_forks_mock.assert_called_once_with(url)
        call_mock.assert_called_once()

    def test_main(self):
        with patch('find_forks.find_forks.find_forks', return_value=None) as find_forks_mock:
            main()
            sent_args = CONFIG.copy()
            sent_args.update({'user': None, 'repo': None, 'no_fetch': False})
            find_forks_mock.assert_called_once_with(**sent_args)

            # Test __version__ exceptions.
            find_forks_mock = MagicMock(side_effect=SystemError())
            del find_forks_mock.__version__
            modules = {
                'find_forks.__init__': find_forks_mock
            }
            with patch.dict('sys.modules', modules):
                self.assertRaises(ImportError, main)
