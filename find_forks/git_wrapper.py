# coding: utf-8
"""Wrappers to interact with git."""
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from .__init__ import CONFIG


def git_fetch_all(**kwargs):
    """Fetch all forks."""
    fetch_all_cmd = 'git fetch --all'
    print(fetch_all_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(fetch_all_cmd.split(' '))


def git_remote_add(name, url, **kwargs):
    """Add fork as git remote."""
    remote_add_cmd = 'git remote add %s %s' % (name, url)
    print(remote_add_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(remote_add_cmd.split(' '))
