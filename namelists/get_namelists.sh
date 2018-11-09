#!/usr/bin/env bash

# make local copies of nml files for runs used in figures

declare -a paths=("$(../figures/exptdata.py)")  # download nmls for runs used in figures

mkdir -p ./raijin

for p in ${paths}; do
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/*/*.nml ./raijin
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/accessom2.nml ./raijin
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/config.yaml ./raijin
done

exit 0
