#!/usr/bin/env python
# coding: utf-8
"""Find forks logic."""
from __future__ import absolute_import, division, print_function, unicode_literals

from argparse import ArgumentParser
import json
import re
import subprocess
import sys

from six import PY3
from six.moves import urllib  # pylint: disable=import-error

CONFIG = {
    'dry_run': False,
    'remote_name': 'origin'
}


def determine_names(remote_name=CONFIG['remote_name'], **kwargs):
    """Try to determine the user and repository name.

    :param remote_name: A clone from github will use "origin" as remote name by default.
    """
    remote_cmd = 'git config --get remote.%s.url' % (remote_name, )
    try:
        origin = subprocess.check_output(remote_cmd.split(' ')).decode('utf-8').strip()
        user, repo = origin.split('/')[-2:]
        repo = repo.rstrip('.git')
    except subprocess.CalledProcessError:
        print('Could not determine user or repo.')
        sys.exit(1)

    return user, repo


def git_remote_add(name, url, **kwargs):
    """Add fork as git remote."""
    remote_add_cmd = 'git remote add %s %s' % (name, url)
    print(remote_add_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(remote_add_cmd.split(' '))


def git_fetch_all(**kwargs):
    """Fetch all forks."""
    fetch_all_cmd = 'git fetch --all'
    print(fetch_all_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(fetch_all_cmd.split(' '))


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
