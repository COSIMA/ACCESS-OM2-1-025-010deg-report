#!/usr/bin/env python

# Automatically update latex tables of namelists for latest runs used in figures

import nmltab  # from https://github.com/aekiss/nmltab
import os, glob, sys

print('Updating table of experiments...')
os.system('python ../figures/exptdata.py --latex >| ../figures/exptdata.tex')

print('Downloading latest namelists for runs used in figures...')
os.system('./get_namelists.sh')

exec(open('../figures/exptdata.py').read())  # do nmls for runs used in figures

nmls = [
    '/ocean/input.nml',
    # '/atmosphere/input_atm.nml',  # MATM: obsolete
    # '/atmosphere/atm.nml',  # TODO: use this when all runs are using YATM
    '/ice/input_ice.nml',
    '/ice/input_ice_gfdl.nml',
    '/ice/input_ice_monin.nml',
    '/ice/cice_in.nml'
    ]

print('Identifying latest runs used in figures...')

configs = []
for e in exptdirs:
    outputs = glob.glob('./raijin' + e + '/output*')
    outputs.sort()
    configs.append(outputs[-1])

print('Updating latex tables of namelists for latest runs used in figures...')
for n in nmls:
    texfname = os.path.basename(n).replace('.', '_') + '.tex'
    st = nmltab.strnmldict(nmltab.nmldict([c + n for c in configs]), format='latex')
    with open(texfname, 'w') as f:
        f.write(st)
    print('   {}'.format(texfname))

configs = ['OFAM3/input.ofam3_spinup03.nml', 'OFAM3/input.ofam2017.nml']
e = exptdict['01deg']['exptdir']
outputs = glob.glob('./raijin' + e + '/output*')
outputs.sort()
configs.append(outputs[-1]+'/ocean/input.nml')
texfname = 'OFAM3_input_nml.tex'
st = nmltab.strnmldict(nmltab.nmldiff(nmltab.nmldict(configs)), format='latex')
with open(texfname, 'w') as f:
    f.write(st)
print('   {}'.format(texfname))

print('Done.')
