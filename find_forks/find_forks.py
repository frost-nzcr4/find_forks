#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import subprocess
import sys

from six import PY3
from six.moves import urllib

user=None
repo=None

github_cmd="git config --get remote.github.url".split(" ")
origin_cmd="git config --get remote.origin.url".split(" ")

# we want to determine the user / repository name
# my convention is that my own projects use 'github' as the remote
# origin when I created it. And, obviously, a clone will use 'origin'.
# so try them each
try:
    github = subprocess.check_output(github_cmd).decode('utf-8').strip()
    user, repo = github.split('/')[-2:]
    user = user.lstrip('git@github.com:')
    repo = repo.rstrip('.git')
except subprocess.CalledProcessError:
    pass  # ok, so no remote called 'github', let's try origin

if user is None and repo is None:
    try:
        origin = subprocess.check_output(origin_cmd).decode('utf-8').strip()
        user, repo = origin.split('/')[-2:]
        repo = repo.rstrip('.git')
    except subprocess.CalledProcessError:
        print("Could not determine user or repo.")
        sys.exit(1)

github_url='https://api.github.com/repos/%s/%s/forks'
resp = urllib.request.urlopen(github_url % (user, repo), timeout=6)
if PY3 and resp.status == 200 or resp.code == 200:
    content = resp.read().decode('utf-8')
    data = json.loads(content)
    for remote in data:
        remote_add_cmd="git remote add %s %s" % (remote['owner']['login'], remote['clone_url'])
        print(remote_add_cmd)
        subprocess.call(remote_add_cmd.split(" "))
fetch_all_cmd="git fetch --all"
print(fetch_all_cmd)
subprocess.call(fetch_all_cmd.split(" "))
