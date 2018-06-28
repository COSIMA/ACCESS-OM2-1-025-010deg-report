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
[[ $HOSTNAME == vdi* ]] || { echo "pushfigs.sh only runs on the VDI."; exit 0; }

basedir='/g/data3/hh5/tmp/cosima/access-om2-report-figures'
uploaddir='figures'
readme=$uploaddir/'README.txt'

dat="$(date +%c)"
dir="$(date -u +%Y-%m-%d_%H%M%SZ)"_"$USER"_"$(git rev-parse --short=7 HEAD)" # unique and informative dir name for each upload
git diff-index --quiet HEAD -- || dir="$dir"-modified
path="$basedir"/versions/"$dir"

# make dummy $basedir/latest symlink if it doesn't exist
if [ ! -L $basedir/latest ]; then
    mkdir -p $basedir/versions/init
    chgrp -R hh5 $basedir/*
    chmod ug+w $basedir/versions
    chmod -R a-w $basedir/versions/init
    ln -sfn $basedir/versions/init $basedir/latest
fi

echo "Uploading "$uploaddir" to "$path" ..."

mkdir -p $path/$uploaddir
echo "Upload failed and may be incomplete." >| $path/$readme  # will be overwritten if successful

# Inherit all previous files (as hard links to save space) so $path contains everything all users have uploaded.
# Exclude $readme so new README.txt doesn't re-use the same hardlinked inode
rsync --archive --no-group --hard-links --one-file-system --exclude $readme --link-dest=$basedir/latest/ $basedir/latest/ $path || { echo "Upload failed."; exit 1; }

# Upload only VDI $uploaddir/* that are newer than (or nonexistent) in shared $path.
rsync -v --archive --no-group --hard-links --one-file-system --update --exclude $readme --link-dest=$basedir/latest/ $uploaddir $path || { echo "Upload failed."; exit 1; }

# make a new README
echo "$path" >| $path/$readme
echo "This contains the shared figure set, updated by "$USER" on ""$dat""." >> $path/$readme
echo "GitHub repository of the commit in use for the update:" >> $path/$readme
echo "https://github.com/OceansAus/ACCESS-OM2-1-025-010deg-report/tree/""$(git rev-parse HEAD)" >> $path/$readme
git diff-index --quiet HEAD -- || echo "(but there were uncommitted local changes)" >> $path/$readme

# make "latest" symlink point to this update 
# NB: new files in repeated failed uploads will not be hardlinked to each other, since symlink won't be updated
ln -sfn $path $basedir/latest || { echo "Error: latest not linked to this upload, so pullfigs.sh won't download it."; exit 1; }

echo "Done."
exit 0
