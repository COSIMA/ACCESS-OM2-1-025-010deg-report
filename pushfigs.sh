#! /bin/sh

# Upload figures from VDI into the shared figure set.
#
# Uploaded figures are stored in $basedir, each upload getting a new directory that
# contains everything previously uploaded by all users, but updated by the new files
# uploaded from the VDI. $basedir/latest is then updated to point to this upload.
# All users can then use pullfigs.sh to fetch the updated figures from $basedir/latest.
#
# Andrew Kiss https://github.com/aekiss

# abort script if $HOSTNAME does not begin with vdi
[[ $HOSTNAME == vdi* ]] || exit 0

# TODO: change basedir to /g/data3/hh5/tmp/cosima/access-om2-report-figures and make it group-writeable
basedir='/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures'

dat="$(date +%c)"
dir="$(date -u +%Y-%m-%d_%H%M%SZ)"_"$USER"_"$(git rev-parse --short=7 HEAD)" # unique and informative dir name for each upload
git diff-index --quiet HEAD -- || dir="$dir"-modified
path="$basedir"/versions/"$dir"

# make dummy $basedir/latest symlink if it doesn't exist
if [ ! -L $basedir/latest ]; then
    mkdir -p $basedir/versions/init/figures
    ln -sfn $basedir/versions/init/figures $basedir/latest
fi

# inherit all previous files (as hard links to save space) so $path contains everything all users have uploaded
mkdir -p $path/figures
rsync --archive --hard-links --one-file-system --link-dest=$basedir/latest/ $basedir/latest/ $path/figures || exit 1

# copy updates across, again using hard links to save space
chmod -R ug+w $path/*
rsync --archive --hard-links --one-file-system --link-dest=$basedir/latest/ figures $path || exit 1

# make a new README
readme=$path/figures/README.txt
rm -f $readme  # so next line doesn't reuse the same hardlinked inode
echo "$path" >| $readme
echo "This contains the shared figure set, updated by "$USER" on ""$dat""." >> $readme
echo "GitHub repository of the commit in use for the update:" >> $readme
echo "https://github.com/OceansAus/ACCESS-OM2-1-025-010deg-report/tree/""$(git rev-parse HEAD)" >> $readme
git diff-index --quiet HEAD -- || echo "(but there were uncommitted local changes)" >> $readme

# read-only for safekeeping - probably overkill
chmod -R a-w $path/*

# make "latest" point to this update 
ln -sfn $path/figures $basedir/latest

exit 0