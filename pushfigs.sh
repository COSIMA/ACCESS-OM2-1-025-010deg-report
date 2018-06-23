#! /bin/sh

# Update shared figure files

# TODO: change basedir to /g/data3/hh5/tmp/cosima/access-om2-report-figures and make it group-writable
basedir='/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures'
# basedir='/Users/andy/Documents/COSIMA/papers/ACCESS-OM2-1-025-010deg'  # for testing

# unique and informative dir name for each upload
dir="$(date -u +%Y-%m-%d_%H%M%SZ)"_"$USER"_"$(git rev-parse --short=7 HEAD)"
git diff-index --quiet HEAD -- || dir="$dir"-modified
path="$basedir"/versions/"$dir"

# make dummy $basedir/latest symlink if it doesn't exist
if [ ! -L $basedir/latest ]; then
    mkdir -p $basedir/versions/init/figures
    ln -sfn $basedir/versions/init/figures $basedir/latest
fi

# inherit all previous files as hard links to save space
mkdir -p $path/figures
rsync --archive --hard-links --one-file-system --link-dest=$basedir/latest/ $basedir/latest/ $path/figures || exit 1

# copy updates across, again using hard links to save space
chmod -R ug+w $path/*
rsync --archive --hard-links --one-file-system --link-dest=$basedir/latest/ figures $path || exit 1

# make a new README
readme=$path/figures/README.txt
rm -f $readme  # so next line doesn't reuse the same hardlinked inode
echo "$path" >| $readme
echo "GitHub repository at the corresponding commit:" >> $readme
echo "https://github.com/OceansAus/ACCESS-OM2-1-025-010deg-report/tree/""$(git rev-parse HEAD)" >> $readme
git diff-index --quiet HEAD -- || echo "but there were additional uncommitted changes" >> $readme

# read-only for safekeeping - probably overkill
chmod -R a-w $path/*

# make "latest" point to this update 
ln -sfn $path/figures $basedir/latest

exit 0