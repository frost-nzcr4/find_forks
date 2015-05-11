#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import re
import subprocess
import sys

from six import PY3
from six.moves import urllib

CONFIG = {
    'dry_run': False
}


def determine_names(remote_name=None):
    """Try to determine the user / repository name."""
    # A clone from github will use "origin" as remote name by default.
    remote_cmd = 'git config --get remote.%s.url' % (remote_name if remote_name else 'origin', )
    try:
        origin = subprocess.check_output(remote_cmd.split(' ')).decode('utf-8').strip()
        user, repo = origin.split('/')[-2:]
        repo = repo.rstrip('.git')
    except subprocess.CalledProcessError:
        print('Could not determine user or repo.')
        sys.exit(1)

    return user, repo


def git_remote_add(name, url):
    """Add fork as git remote."""
    remote_add_cmd = 'git remote add %s %s' % (name, url)
    print(remote_add_cmd)
    if not CONFIG['dry_run']:
        subprocess.call(remote_add_cmd.split(' '))


def git_fetch_all():
    """Fetch all forks."""
    fetch_all_cmd = 'git fetch --all'
    print(fetch_all_cmd)
    if not CONFIG['dry_run']:
        subprocess.call(fetch_all_cmd.split(' '))


def add_forks(url, follow_next=True):
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
            git_remote_add(fork['owner']['login'], fork['clone_url'])
        # Gets link to next page.
        if follow_next:
            link = response.getheader('Link', '') if PY3 else dict(response.info()).get('link', '')
            match = re.match(r'<(.*)>;\ rel="next"', link)
            if match:
                return match.group(1)

    return None


def find_forks():
    """Find forks.

    Runs all methods in proper order to find all forks of github user/repo."""
    user, repo = determine_names()

    url = 'https://api.github.com/repos/%s/%s/forks' % (user, repo)
    while url:
        url = add_forks(url)

    git_fetch_all()

if __name__ == '__main__':
    find_forks()
