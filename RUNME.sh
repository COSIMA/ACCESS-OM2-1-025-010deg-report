#!/usr/bin/env sh

# copies git hooks to .git/hooks so that gitinfo package works
cp cp_to_git_hooks/* .git/hooks
git checkout
exit 0