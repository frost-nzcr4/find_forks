#!/usr/bin/env python
# coding: utf-8
"""Find forks logic."""
from __future__ import absolute_import, division, print_function, unicode_literals

from argparse import ArgumentParser
import json
import logging
import re

from six import PY3
from six.moves import urllib  # pylint: disable=import-error

from .__init__ import CONFIG
from .git_wrapper import git_config_get_remote, git_fetch_all, git_remote_add
from .interesting import add_interesting_fork, print_interesting_forks


log = logging.getLogger(__name__)


def determine_names(remote_name=CONFIG['remote_name'], **kwargs):  # TRICKY: kwargs is used to prevent TypeError when it got an unexpected keyword argument from find_forks(). pylint: disable=unused-argument
    """Try to determine the user and repository name.

    :param remote_name: A clone from github will use "origin" as remote name by default.

    Returns list with user and repo.
    """
    remote_url = git_config_get_remote(remote_name)
    if not remote_url:
        raise RuntimeError('Could not get remote url with name "%s". Check output of your `git remote`.' % (remote_name, ))

    remote_url = remote_url[15:] if 'git@github.com:' == remote_url[0:15] else remote_url
    remote_url = remote_url[:-4] if '.git' == remote_url[-4:] else remote_url

    return remote_url.split('/')[-2:]


def add_forks(url, follow_next=True, **kwargs):
    """Add forks to the current project."""
    log.info('Open %s', url)
    try:
        response = urllib.request.urlopen(url, timeout=6)
    except urllib.error.URLError as ex:
        log.error(ex)
        return None

    if PY3 and response.status == 200 or response.code == 200:
        content = response.read().decode('utf-8')
        forks = json.loads(content)
        for fork in forks:
            add_interesting_fork(fork)
            git_remote_add(fork['owner']['login'], fork['clone_url'], **kwargs)
        # Gets link to next page.
        if follow_next:
            link = response.getheader('Link', '') if PY3 else dict(response.info()).get('link', '')
            match = re.search(r'<([^<]*)>;\ rel="next"', link)
            if match:
                return match.group(1)

    return None


def find_forks(user=None, repo=None, determine_names_handler=None, per_page=CONFIG['per_page'], start_page=CONFIG['start_page'], **kwargs):
    """Find forks.

    Runs all methods in proper order to find all forks of github user/repo."""
    if user is None and repo is None:
        user, repo = determine_names(**kwargs) if determine_names_handler is None else determine_names_handler(**kwargs)

    url = 'https://api.github.com/repos/%s/%s/forks?per_page=%s&page=%s' % (user, repo, per_page, start_page)
    while url:
        url = add_forks(url, **kwargs)

    if not kwargs.get('no_fetch', False):
        git_fetch_all(**kwargs)


def main():
    """Main function to run as shell script."""
    try:
        from .__init__ import __version__
    except (SystemError, ValueError) as ex:
        if PY3 and isinstance(ex, SystemError) or isinstance(ex, ValueError):
            from __init__ import __version__  # pylint: disable=import-error,no-name-in-module
        else:
            raise

    parser = ArgumentParser(prog='find_forks')
    parser.add_argument(
        '-n', '--remote-name', default=CONFIG['remote_name'],
        help='Specify git remote name to determine user and repo (default: %s)' % (CONFIG['remote_name'], ))
    parser.add_argument('-l', '--log', default='info', help='Specify log level (notset, debug, info, warning, error, critical)')
    parser.add_argument('--no-fetch', default=False, action='store_true', help='Do not run git fetch to run it manually later')
    parser.add_argument('-u', '--user', default=None, help='Specify github user')
    parser.add_argument('-r', '--repo', default=None, help='Specify github user\'s repo')
    parser.add_argument('-p', '--per-page', default=CONFIG['per_page'], help='Specify number of records per page on github')
    parser.add_argument('-s', '--start-page', default=CONFIG['start_page'], help='Specify start page on github')
    parser.add_argument('--dry-run', default=CONFIG['dry_run'], action='store_true', help='Do not run the git commands')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()

    if args.log:
        root_log = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s %(name)s:%(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        root_log.addHandler(handler)
        root_log.setLevel(args.log.upper())
    del args.log

    find_forks(**vars(args))
    print_interesting_forks()

if __name__ == '__main__':
    main()
