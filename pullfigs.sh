#! /bin/sh

# Download latest files from the shared set (uploaded from VDI by pushfigs.sh)
#
# Andrew Kiss https://github.com/aekiss

basedir='/g/data3/hh5/tmp/cosima/access-om2-report-figures'
figsdir=$basedir/latest

echo "Checking for updated files in "$figsdir
# TODO: store uname in ~/.pullfigs.conf and only ask for it if this file is absent
read -p "NCI username: " uname

# Download everything in latest shared dir that's newer than (or nonexistent) locally
# include only files that are in .gitignore (the others will be handled by git)
# TODO: download new .ipynb to ensure they don't get stranded on VDI with only the .pdfs shared? But what if they aren't ready to share?

# First to  dry run to confirm the changes that would occur
# rsync $rsyncopts --dry-run $uname@r-dm.nci.org.au:$basedir/latest/ . || exit 1
rsync -aPSH  --no-perms --no-owner --no-group  --update --exclude '_*' --exclude '.*'  --include '*/' --include 'README.txt' --include '*.pdf' --include '*.png' --exclude '*' --dry-run $uname@r-dm.nci.org.au:$basedir/latest/ . || exit 1
echo "Caution: If any of the above files already exist locally they will be overwritten by these updates."
read -p "Proceed anyway? (y/n) " yesno
case $yesno in
    [Yy]* ) break;;
    * ) echo "Download cancelled. No files were changed."; exit 0;;
esac

# now do update
rsync -aPSH  --no-perms --no-owner --no-group  --update --exclude '_*' --exclude '.*'  --include '*/' --include 'README.txt' --include '*.pdf' --include '*.png' --exclude '*' $uname@r-dm.nci.org.au:$basedir/latest/ . || exit 1

echo "Done."

exit 0