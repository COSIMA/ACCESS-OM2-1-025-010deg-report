#! /bin/sh

# Download latest figures from the shared figure set (uploaded from VDI by pushfigs.sh)
#
# Andrew Kiss https://github.com/aekiss

# TODO: change basedir to /g/data3/hh5/tmp/cosima/access-om2-report-figures and make it group-writeable
basedir='/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures'

# TODO: don't hardcode username

# rsync -aPSH --exclude '*.ipynb' --exclude '*.py' --exclude '.*' --exclude '_*' aek156@r-dm.nci.org.au:/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures/latest/ ./figures

# include only files that are in .gitignore (the others will be handled by git)
rsync -aPSH  --no-perms --no-owner --no-group --include '*/' --include 'README.txt' --include '*.pdf' --include '*.png' --exclude '*' aek156@r-dm.nci.org.au:/g/data3/hh5/tmp/cosima/access-om2-01/access-om2-report-figures/latest/ ./figures

exit 0