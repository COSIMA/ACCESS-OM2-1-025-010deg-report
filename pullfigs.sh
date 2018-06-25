#! /bin/sh

# Download latest figures from the shared figure set (uploaded from VDI by pushfigs.sh)
#
# Andrew Kiss https://github.com/aekiss

basedir='/g/data3/hh5/tmp/cosima/access-om2-report-figures'

# TODO: don't hardcode username

# rsync -aPSH --exclude '*.ipynb' --exclude '*.py' --exclude '.*' --exclude '_*' aek156@r-dm.nci.org.au:/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures/latest/ ./figures

# Download everything in latest shared dir that's newer than (or nonexistent) 
# in local figures/
# include only files that are in .gitignore (the others will be handled by git)
# TODO: download new .ipynb to ensure they don't get stranded on VDI with only the .pdfs shared? But what if they aren't ready to share?
rsync -aPSH  --no-perms --no-owner --no-group  --update --include '*/' --include 'README.txt' --include '*.pdf' --include '*.png' --exclude '*' aek156@r-dm.nci.org.au:$basedir/latest/ ./figures

exit 0