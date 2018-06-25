#!/usr/bin/env sh

# copy git hooks to .git/hooks so that gitinfo package works
cp git-hooks/gitinfo-git-hook.txt .git/hooks/post-checkout
cp git-hooks/gitinfo-git-hook.txt .git/hooks/post-commit
cp git-hooks/gitinfo-git-hook.txt .git/hooks/post-merge
chmod +x .git/hooks/post-checkout
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/post-merge
# and make .git/gitHeadInfo.git for gitinfo package
git checkout

# # set up pushfigs hook
# cp git-hooks/pushfigs-git-hook.txt .git/hooks/pre-push
# chmod +x .git/hooks/pre-push
# chmod +x pushfigs.sh
# chmod +x pullfigs.sh
# 
# # append pullfigs to post-merge hook
# echo "exec ./pullfigs.sh" >> .git/hooks/post-merge

exit 0