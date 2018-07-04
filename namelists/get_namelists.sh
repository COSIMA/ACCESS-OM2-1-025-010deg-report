#!/usr/bin/env bash

# make local copies of nml files

declare -a paths=("$(../figures/exptdata.py)")  # download nmls for runs used in figures

mkdir -p ./raijin

for p in ${paths}; do
    nice time rsync -avPSRH aek156@r-dm.nci.org.au:$p/output*/*/*.nml ./raijin
done

exit 0
