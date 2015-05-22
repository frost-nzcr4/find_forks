#!/usr/bin/env python
# coding: utf-8
"""Find forks logic."""
from __future__ import absolute_import, division, print_function, unicode_literals

from argparse import ArgumentParser
import json
import re

from six import PY3
from six.moves import urllib  # pylint: disable=import-error

from .__init__ import CONFIG
from .git_wrapper import git_config_get_remote, git_fetch_all, git_remote_add


def determine_names(remote_name=CONFIG['remote_name'], **kwargs):
    """Try to determine the user and repository name.

    :param remote_name: A clone from github will use "origin" as remote name by default.

    Returns list with user and repo.
    """
    remote_url = git_config_get_remote(remote_name)
    if not remote_url:
        raise RuntimeError('Could not get remote url with name "%s". Check output of your `git remote`.' % (remote_name, ))

    return remote_url.rstrip('.git').split('/')[-2:]


def add_forks(url, follow_next=True, **kwargs):
    """Add forks to the current project."""
    print('Open %s' % url)
    try:
        response = urllib.request.urlopen(url, timeout=6)
    except urllib.error.URLError as ex:
        print('Error: %s' % (ex.reason, ))
        return None

    if PY3 and response.status == 200 or response.code == 200:
        content = response.read().decode('utf-8')
        forks = json.loads(content)
        for fork in forks:
            git_remote_add(fork['owner']['login'], fork['clone_url'], **kwargs)
        # Gets link to next page.
        if follow_next:
            link = response.getheader('Link', '') if PY3 else dict(response.info()).get('link', '')
            match = re.match(r'<(.*)>;\ rel="next"', link)
            if match:
                return match.group(1)

    return None


def find_forks(user=None, repo=None, determine_names_handler=None, per_page=100, **kwargs):
    """Find forks.

    Runs all methods in proper order to find all forks of github user/repo."""
    if user is None and repo is None:
        user, repo = determine_names(**kwargs) if determine_names_handler is None else determine_names_handler(**kwargs)

    url = 'https://api.github.com/repos/%s/%s/forks?per_page=%s' % (user, repo, per_page)
    while url:
        url = add_forks(url, **kwargs)

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
    parser.add_argument('-u', '--user', default=None, help='Specify github user')
    parser.add_argument('-r', '--repo', default=None, help='Specify github user\'s repo')
    parser.add_argument('--dry-run', default=CONFIG['dry_run'], action='store_true', help='Do not run the git commands')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()

    find_forks(**vars(args))

if __name__ == '__main__':
    main()
