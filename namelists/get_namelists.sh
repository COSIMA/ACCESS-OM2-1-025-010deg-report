#!/usr/bin/env bash

# get latest control dirs from github

herepath=$(pwd)
gitpath=github.com/COSIMA
branch=ak-dev

mkdir -p $gitpath

declare -a repos=("01deg_jra55_iaf" "01deg_jra55_ryf" "025deg_jra55_ryf" "025deg_jra55_iaf" "1deg_jra55_iaf" "1deg_jra55_ryf")
for r in ${repos[@]}; do
    git clone https://$gitpath/$r.git $gitpath/$r || true
    cd $gitpath/$r
    git checkout origin/$branch
    git checkout $branch
    git pull origin $branch
    cd $herepath
done


# make local copies of nml files for runs used in figures

declare -a paths=("$(../figures/exptdata.py)")  # nmls for runs used in figures
paths=("${paths[@]}" "/g/data/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf9091")  # append new RYF spinup
paths=("${paths[@]}" "/g/data/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6_000-413")  # append early RYF spinup6 files
mkdir -p ./gadi

for p in ${paths[@]}; do
    echo $p
    nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:$p/output*/*/*.nml ./gadi
    nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:$p/output*/accessom2.nml ./gadi
    nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:$p/output*/config.yaml ./gadi
    nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:$p/output*/ocean/field_table ./gadi
done

# copy spinup6_000-413 files to spinup6 (NB: this will no longer match remote spinup6)
rsync -avPSH ./gadi/g/data/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6_000-413/* ./gadi/g/data/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6

# also get namelists Marshall used for performance tests
nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:/g/data/hh5/tmp/cosima/raijin-short-public/mxw900/home/mxw157/om2bench/*/*/*.nml ./gadi
nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:/g/data/hh5/tmp/cosima/raijin-short-public/mxw900/home/mxw157/om2bench/*/*/*/*.nml ./gadi
# nice time rsync -avPSRH aek156@gadi-dm.nci.org.au:/g/data/hh5/tmp/cosima/raijin-short-public/mxw900/home/mxw157/om2bench/*/*/*/*/*.nml ./gadi

exit 0
