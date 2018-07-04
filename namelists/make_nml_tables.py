#!/usr/bin/env python

# Automatically generate latex tables of namelists

import nmltab  # from https://github.com/aekiss/nmltab
import os, glob
exec(open('../figures/exptdata.py').read())  # do nmls for runs used in figures

source = 'local'

nmls = [
    '/ocean/input.nml',
    # '/atmosphere/input_atm.nml',
    '/ice/input_ice.nml',
    '/ice/input_ice_gfdl.nml',
    '/ice/input_ice_monin.nml',
    '/ice/cice_in.nml'
    ]

if source=='raijin':
    prefix = '/Volumes/aek156@r-dm.nci.org.au'  # for my FUSE mount
    
    configs = [  # on raijin
        '/short/v45/amh157/access-om2/control/1deg_jra55_ryf',
        # '/short/v45/amh157/access-om2/control/1deg_jra55_ryf_RCP45'
        '/short/v45/aek156/access-om2/control/025deg_jra55_ryf',
        '/short/v45/amh157/access-om2/control/01deg_jra55_ryf'
        ]

    configs = [  # on raijin, updated 2018-06-27
        '/g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf8485_kds50_may/output060',
        '/g/data3/hh5/tmp/cosima/access-om2-025/025deg_jra55v13_ryf8485_spinup_A/output099',
        '/g/data3/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6'
        ]
else:
    prefix = ''
    
    configs = [  # local
        '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/1deg_jra55_ryf',
        '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/025deg_jra55_ryf',
        '/Users/andy/Documents/COSIMA/github/OceansAus/access-om2/control/01deg_jra55_ryf'
        ]

    configs = [  # local, updated 2018-06-27
        '/Users/andy/Documents/COSIMA/github/aekiss/namelist-check/raijin/g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf8485_kds50_may/output060',
        '/Users/andy/Documents/COSIMA/github/aekiss/namelist-check/raijin/g/data3/hh5/tmp/cosima/access-om2-025/025deg_jra55v13_ryf8485_spinup_A/output099',
        '/Users/andy/Documents/COSIMA/github/aekiss/namelist-check/raijin/g/data3/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6'
        ]
    
    configs = [  # local raijin mirror, updated 2018-06-27
        './raijin/g/data3/hh5/tmp/cosima/access-om2/1deg_jra55_ryf8485_kds50_may/output060',
        './raijin/g/data3/hh5/tmp/cosima/access-om2-025/025deg_jra55v13_ryf8485_spinup_A/output099',
        './raijin/g/data3/hh5/tmp/cosima/access-om2-01/01deg_jra55v13_ryf8485_spinup6/output403'
        ]
    
    # use latest runs used in figures
    configs = []
    for e in exptdirs:
        outputs = glob.glob('./raijin' + e + '/output*')
        outputs.sort()
        configs.append(outputs[-1])

for n in nmls:
    st = nmltab.strnmldict(nmltab.nmldict([prefix + c + n for c in configs]), format='latex')
    with open(os.path.basename(n).replace('.', '_') + '.tex', 'w') as f:
        f.write(st)
