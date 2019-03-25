#!/usr/bin/env bash

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
