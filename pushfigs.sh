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

basedir='/g/data/hh5/tmp/cosima/access-om2-report-figures'
uploaddir='figures'
readme=$uploaddir/'README.txt'

dat="$(date +%c)"
dir="$(date -u +%Y-%m-%d_%H%M%SZ)"_"$USER"_"$(git rev-parse --short=7 HEAD)" # unique and informative dir name for each upload
if [ -n "$(git status --porcelain)" ]; then
# uncommitted changes or untracked files
    dir="$dir"-modified
fi
path="$basedir"/versions/failed/"$dir"
finalpath="$basedir"/versions/"$dir"

# make dummy $basedir/latest symlink if it doesn't exist
if [ ! -L $basedir/latest ]; then
    mkdir -p $basedir/versions/init
    mkdir -p $basedir/versions/failed
    chgrp -R hh5 $basedir/versions
    chmod -R ug+w $basedir/versions
    ln -sfn $basedir/versions/init $basedir/latest
fi

mkdir -p $path/$uploaddir || { echo "Upload failed."; exit 1; }
echo "Upload failed and may be incomplete." >| $path/$readme  # will be overwritten if successful

# Upload only VDI $uploaddir/* that differ from (or don't exist in) --link-dest (even if those in --link-dest are newer).
# Note that this won't inherit any files from --link-dest that the uploading user doesn't have.
echo "Finding modified files to upload ..."
rsync --dry-run -i --archive --no-group --no-owner --no-perms --chmod="g+w" --one-file-system --exclude $readme  --exclude '.*' --exclude '.*/' --exclude 'NOSYNC' --exclude dask-worker-space --exclude __pycache__ --exclude cache_* --link-dest=$basedir/latest/ ./$uploaddir $path || { echo "Upload failed."; exit 1; }

read -p "Upload these files to shared directory? (y/n) " yesno
case $yesno in
    [Yy] ) break;;
    * ) echo "Upload cancelled."; exit 0;;
esac

echo "Uploading ./"$uploaddir" to "$path" ..."
rsync -i --archive --no-group --no-owner --no-perms --chmod="g+w" --one-file-system --exclude $readme  --exclude '.*' --exclude '.*/' --exclude 'NOSYNC' --exclude dask-worker-space --exclude __pycache__ --exclude cache_* --link-dest=$basedir/latest/ ./$uploaddir $path || { echo "Upload failed."; exit 1; }

# fix group of all files owned by this user (the rest are older files and hopefully already fixed up)
# in newer rsync versions this could be done by --chown=":hh5" or --groupmap="*:hh5"
chgrp -R hh5 $path > /dev/null 2>&1

# Inherit all previous files (as hard links to save space) so $path contains everything all users have uploaded.
# Will overwite files in $path with those in --link-dest if --link-dest ones are newer.
# Exclude $readme so new README.txt doesn't re-use the same hardlinked inode.
echo "Adding all newer or additional files from previous uploads..."
rsync -i --archive --no-group --no-perms --hard-links --one-file-system --update --exclude $readme --link-dest=$basedir/latest/ $basedir/latest/ $path || { echo "Upload failed."; exit 1; }

# make a new README
echo "Updating "$readme" ..."
echo "$finalpath" >| $path/$readme
echo "This contains the shared figure set, updated by "$USER" on ""$dat""." >> $path/$readme
echo "GitHub repository of the commit in use for the update:" >> $path/$readme
echo "https://github.com/OceansAus/ACCESS-OM2-1-025-010deg-report/tree/""$(git rev-parse HEAD)" >> $path/$readme
if [ -n "$(git status --porcelain)" ]; then
    echo "(but there were uncommitted local changes and/or untracked files)" >> $path/$readme
fi

echo "Moving upload to "$finalpath" ..."
mv $path $finalpath || { echo "Upload failed."; exit 1; }

# make "latest" symlink point to this update 
# NB: new files in repeated failed uploads will not be hardlinked to each other, since symlink won't be updated
ln -sfn $finalpath $basedir/latest || { echo "Error: latest not linked to this upload, so pullfigs.sh won't download it."; exit 1; }
echo "Linked "$basedir/latest" to "$finalpath

echo "Upload completed. Contributors can download the latest versions of all .pdf and .png files using pullfigs.sh."
if [ -n "$(git status --porcelain)" ]; then
    echo "There are uncommitted changes and/or untracked files. Please use git to add, commit and push your latest notebook versions so we can track how these figures were created."
fi

exit 0
