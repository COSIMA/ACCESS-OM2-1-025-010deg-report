#!/usr/bin/env sh

# copy git hooks to .git/hooks so that gitinfo package works
cp gitinfo-git-hook.txt .git/hooks/post-checkout
cp gitinfo-git-hook.txt .git/hooks/post-commit
cp gitinfo-git-hook.txt .git/hooks/post-merge
# and make .git/gitHeadInfo.git for gitinfo package
git checkout
exit 0