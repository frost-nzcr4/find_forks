#!/bin/bash
#
# Remove duplicate branches.
#
# Run it after find_forks gets done.
#

if [ "$1" == "" ]; then
    echo "You should specify your github name as first argument"
    exit 1
fi

GITHUB_NAME="$1"

for BRANCH in $( git branch -r --no-color | cut -d" " -f3 ); do
    # Is that branch exists?
    if [ `git branch -r --no-color --list "$BRANCH" | cut -d" " -f3` ]; then
        for MERGED_BRANCH in $( git branch -r --no-color --merged "$BRANCH" | cut -d" " -f3  | grep -v -e "\(origin\|upstream\|$GITHUB_NAME\)/"); do
            if [ "$MERGED_BRANCH" != "$BRANCH" ]; then
                git branch -r -d "$MERGED_BRANCH"
            fi
        done
    fi
done
