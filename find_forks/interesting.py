# coding: utf-8
"""Find interesting forks."""
from __future__ import absolute_import, division, print_function, unicode_literals

from six import PY3


INTERESTING_FORKS = []


def add_interesting_fork(fork):
    """Add interesting fork to list."""
    if fork['forks_count'] or fork['stargazers_count'] or fork['watchers_count']:
        INTERESTING_FORKS.append((fork['owner']['login'], fork['forks_count'], fork['stargazers_count'], fork['watchers_count']))


def print_interesting_forks(sort=None, custom_sorting_rules=None, width=32):
    """Print interesting forks table.

    :param sort: string or list with columns to sort (default None)
    :param custom_sorting_rules: dict with rules (default None)
    :param width: integer to generate fixed width string when printing (default 32)

    Examples::

    print_interesting_forks(('watchers', 'forks'))
    if one's need to sort forks list by watchers count and then forks count.

    print_interesting_forks('my_rule', {'my_rule': lambda x: x[1] * 4 + x[2] * 2 + x[3]})
    If one's set custom_sorting_rules argument, each custom sorting rule gets tuple on input where
    x[1] -- forks count
    x[2] -- stargazers count
    x[3] -- watchers count
    """
    global INTERESTING_FORKS  # NOTE: Do not disable it with pylint.
    sorting_rules = {
        'sum': lambda x: x[1] + x[2] + x[3],
        'forks': lambda x: x[1],
        'stargazers': lambda x: x[2],
        'watchers': lambda x: x[3]
    }
    if custom_sorting_rules:
        sorting_rules.update(custom_sorting_rules)

    if not INTERESTING_FORKS:
        print('There are no interesting forks')
        return None

    print('Possible interesting forks')
    print('%s | forks | stargazers | watchers' % (' ' * width))
    print('-' * (width + 32))

    sort = 'sum' if sort is None else sort
    sort = [i for i in sort] if hasattr(sort, '__iter__') and (not PY3 or PY3 and not isinstance(sort, str)) else [sort]

    sort.reverse()
    for rule in sort:
        INTERESTING_FORKS = sorted(INTERESTING_FORKS, key=sorting_rules[rule], reverse=True)

    for fork in INTERESTING_FORKS:
        row_format = '%' + str(width) + 's | %4s | %4s | %4s'
        print(row_format % (fork[0][0:width], fork[1], fork[2], fork[3]))
