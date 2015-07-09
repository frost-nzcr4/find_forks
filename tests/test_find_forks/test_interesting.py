# coding: utf-8
"""test_find_fork."""
# pylint: disable=no-self-use
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from os import path

from find_forks.interesting import print_interesting_forks

from .__init__ import BASEPATH
from .test_find_forks import FindForksCommon


class InterestingTest(FindForksCommon):
    def test_print_interesting_forks(self):
        print_interesting_forks(sort='my_rule', custom_sorting_rules={'my_rule': lambda x: x[3]})

        with open(path.join(BASEPATH, 'fixture/response.json')) as fixture:
            json_obj = json.load(fixture)
        json_obj[0].update({
            'forks_count': 1,
            'watchers_count': 2,
            'stargazers_count': 3
        })
        json_response = json.dumps(json_obj).encode('utf-8')
        response_mock = self.make_mock(json_response)
        self.make_test(response_mock)

        print_interesting_forks()
