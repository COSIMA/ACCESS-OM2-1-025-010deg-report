#!/usr/bin/env python

# Automatically generate latex tables of namelists

import nmltab  # from https://github.com/aekiss/nmltab
import os

nmls = [
    '/ocean/input.nml',
    '/atmosphere/input_atm.nml',
    '/ice/input_ice.nml',
    '/ice/input_ice_gfdl.nml',
    '/ice/input_ice_monin.nml',
    '/ice/cice_in.nml'
    ]

configs = [  # on raijin
    '/short/v45/amh157/access-om2/control/1deg_jra55_ryf',
    # '/short/v45/amh157/access-om2/control/1deg_jra55_ryf_RCP45'
    '/short/v45/aek156/access-om2/control/025deg_jra55_ryf',
    '/short/v45/amh157/access-om2/control/01deg_jra55_ryf'
    ]

configs = [  # local
    '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/1deg_jra55_ryf',
    '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/025deg_jra55_ryf',
    '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/01deg_jra55_ryf'
    ]

for n in nmls:
    st = nmltab.strnmldict(nmltab.nmldict([c + n for c in configs]), format='latex')
    with open(os.path.basename(n).replace('.', '_') + '.tex', 'w') as f:
        f.write(st)
