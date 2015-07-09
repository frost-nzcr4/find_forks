# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
import unittest

from six import PY3

from find_forks.__init__ import CONFIG
from find_forks.find_forks import add_forks, determine_names, find_forks, main

from .__init__ import BASEPATH

if PY3:
    from unittest.mock import patch, MagicMock, Mock  # pylint: disable=no-name-in-module
else:
    from mock import patch, MagicMock, Mock


class FindForksCommon(unittest.TestCase):
    @staticmethod
    def make_mock(json_response):
        """Used in test_interesting.py."""
        response_mock = MagicMock()
        response_mock.read = Mock(return_value=json_response)
        if PY3:
            response_mock.status = 200
            response_mock.getheader = Mock(return_value='<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2>; rel="next", '
                                           '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=3>; rel="last"')
        else:
            response_mock.code = 200
            response_mock.info = Mock(return_value=(('link', '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2>; rel="next", '
                                                             '<https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=3>; rel="last"'), ))

        return response_mock

    def make_test(self, response_mock):
        """Used in test_interesting.py."""
        url = 'https://github.com/frost-nzcr4/find_forks'
        with patch('find_forks.find_forks.urllib.request.urlopen', return_value=response_mock) as urlopen_mock:
            with patch('find_forks.git_wrapper.subprocess.call', return_value=None):
                self.assertEqual(add_forks(url), 'https://api.github.com/repos/frost-nzcr4/find_forks/forks?page=2')
                urlopen_mock.assert_called_once_with(url, timeout=6)
                if PY3:
                    response_mock.status = 404
                else:
                    response_mock.code = 404
                self.assertIsNone(add_forks(url))


class FindForksTest(FindForksCommon):
    def test_add_forks(self):
        self.assertIsNone(add_forks('httttps://unavailable!url'))

        with open(path.join(BASEPATH, 'fixture/response.json'), 'rb') as fixture:
            json_response = fixture.read()
        response_mock = self.make_mock(json_response)
        self.make_test(response_mock)

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
