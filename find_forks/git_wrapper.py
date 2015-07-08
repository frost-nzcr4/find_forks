# coding: utf-8
"""Wrappers to interact with git."""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import subprocess

from .__init__ import CONFIG


log = logging.getLogger(__name__)


def git_config_get_remote(remote_name=None):
    """Get remote url from config."""
    config_get_remote_cmd = 'git config --get remote.%s.url' % (remote_name, )
    log.debug(config_get_remote_cmd)
    try:
        remote_url = subprocess.check_output(config_get_remote_cmd.split(' ')).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

    return remote_url


def git_fetch_all(**kwargs):
    """Fetch all forks."""
    fetch_all_cmd = 'git fetch --all'
    log.debug(fetch_all_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(fetch_all_cmd.split(' '))


def git_remote_add(name, url, **kwargs):
    """Add fork as git remote."""
    remote_add_cmd = 'git remote add %s %s' % (name, url)
    log.debug(remote_add_cmd)
    if not kwargs.get('dry_run', CONFIG['dry_run']):
        subprocess.call(remote_add_cmd.split(' '))
