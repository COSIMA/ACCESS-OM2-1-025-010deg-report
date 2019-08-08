#!/usr/bin/env bash

# get latest control dirs from github

herepath=$(pwd)
gitpath=github.com/COSIMA
branch=ak-dev

mkdir -p $gitpath

declare -a repos=("01deg_jra55_iaf" "01deg_jra55_ryf" "minimal_01deg_jra55_iaf" "minimal_01deg_jra55_ryf" "025deg_core2_nyf" "025deg_jra55_ryf" "025deg_jra55_iaf" "1deg_core_nyf" "1deg_jra55_iaf" "1deg_jra55_ryf")
for r in ${repos[@]}; do
    git clone https://$gitpath/$r.git $gitpath/$r || true
    cd $gitpath/$r
    git checkout origin/$branch
    git checkout $branch
    git pull origin $branch
    cd $herepath
done


# make local copies of nml files for runs used in figures

declare -a paths=("$(../figures/exptdata.py)")  # download nmls for runs used in figures

mkdir -p ./raijin

for p in ${paths}; do
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/*/*.nml ./raijin
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/accessom2.nml ./raijin
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/config.yaml ./raijin
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/ocean/field_table ./raijin
done

# also get namelists Marshall used for performance tests
nice time rsync -avPSRH aek156@r-dm.nci.org.au:/short/public/mxw900/home/mxw157/om2bench/*/*/*.nml ./raijin
nice time rsync -avPSRH aek156@r-dm.nci.org.au:/short/public/mxw900/home/mxw157/om2bench/*/*/*/*.nml ./raijin
nice time rsync -avPSRH aek156@r-dm.nci.org.au:/short/public/mxw900/home/mxw157/om2bench/*/*/*/*/*.nml ./raijin

exit 0
