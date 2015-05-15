find_forks
==========

Finds all forks of user/repo on github and add it as `git remote` to your local cloned repo.
Useful to find interesting commits of:

* old repo with many updated forks,
* fresh repo with many forks that original author doesn't want or doesn't have time to merge.

## Install

You need `python` (3.4.2 and 2.7.8 tested) and `pip` installed.

```ShellSession
git clone --branch master https://github.com/frost-nzcr4/find_forks.git
cd find_forks
pip install -r requirements-prod.txt
```

## Usage

### Basics

1. Run as console comand:

   At first you need some cloned project and `cd` to one's root:

   ```ShellSession
   git clone https://github.com/some_user/some_project.git
   cd some_project
   ```

   Now you can run `find_forks` one of the following methods:

   * specify path to folder:

     ```ShellSession
     python /path/to/find_forks
     ```

   * specify module name If `find_forks` in your PYTHONPATH:

     ```ShellSession
     python -m find_forks
     ```

   * or if you obtained zip from github you could simply run it:

     ```ShellSession
     python /path/to/find_forks.zip
     ```

   You can provide arguments to get forks of specified user/repo:

   ```ShellSession
   python /path/to/find_forks --user=user --repo=repo
   ```


2. Use as module:

   ```python
   from find_forks.find_forks import find_forks

   find_forks()
   ```

### Define your own name determination handler

```python
from find_forks.find_forks import determine_names, find_forks


def my_handler():
    """Your own handler."""
    # Do something.
    
    # If something goes wrong you can run default handler, just uncomment following line.
    #return determine_names()

    # This is mandatory. Your handler should return user and repo names.
    return user, repo

find_forks(determine_names_handler=my_handler):
```

## How to contribute

Install additional development requirements:

```ShellSession
pip install -r requirements-dev.txt
```

Before you start to pull request your changes on github please run tests to make sure that nothing went wrong:

```ShellSession
./tests/run.py
```

and check that result doesn't break python code conventions:

```ShellSession
pep8
pylint __main__.py find_forks
pylint -d C0111 tests
```

Check coverage if you needed it:

```ShellSession
coverage run tests/run.py
coverage html
```

then open `tests/coverage/html_report/index.html` with your browser.

## License & Authors

When I needed `find_forks` functionality I'd start to search for available projects and found [gist](https://gist.github.com/akumria/3405534) of Anand Kumria (@akumria) which I used as starting point to this module.

Copyright (c) 2015 Alexander Pervakov

See the file "LICENSE" for information on terms & conditions for usage.
