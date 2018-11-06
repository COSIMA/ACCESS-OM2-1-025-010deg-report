#!/usr/bin/env python

# Automatically update latex tables of namelists for latest runs used in figures

import nmltab  # from https://github.com/aekiss/nmltab
import os
import glob
import yaml

print('Updating table of experiments...')
os.system('python ../figures/exptdata.py --latex >| ../figures/exptdata.tex')

print('Downloading latest namelists for runs used in figures...')
os.system('./get_namelists.sh')

exec(open('../figures/exptdata.py').read())  # do nmls for runs used in figures

nmls = [
    '/accessom2.nml',
    '/ocean/input.nml',
    # '/atmosphere/input_atm.nml',  # MATM: obsolete
    '/atmosphere/atm.nml',  # TODO: use this when all runs are using YATM
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

configs2 = ['OFAM3/input.ofam3_spinup03.nml', 'OFAM3/input.ofam2017.nml']
e = exptdict['01deg']['exptdir']
outputs = glob.glob('./raijin' + e + '/output*')
outputs.sort()
configs2.append(outputs[-1]+'/ocean/input.nml')
texfname = 'OFAM3_input_nml.tex'
st = nmltab.strnmldict(nmltab.nmldiff(nmltab.nmldict(configs2)), format='latex')
with open(texfname, 'w') as f:
    f.write(st)
print('   {}'.format(texfname))

print('Making table of input paths...')
parsed_configs = dict()
for c in configs:
    with open(c + '/config.yaml', 'r') as infile:
        parsed_configs[c] = yaml.load(infile)
    parsed_configs[c]['submodels-by-name'] = dict()
    for sm in parsed_configs[c]['submodels']:
        parsed_configs[c]['submodels-by-name'][sm['name']] = sm
with open('config_inputs.tex', 'w') as f:
    f.write(r'\begin{tabularx}{\linewidth}{l')
    f.write(r'p{0.3\linewidth}'*len(configs))
    f.write('}\n\\hline\n & \\textbf{')
    f.write(r'} & \textbf{'.join(descs))
    f.write(r'}\\' + '\n\\hline\n')
    rowstr = '{} & ' + r'\texttt{{{}}} & '*(len(configs)-1) + r'\texttt{{{}}}\\' + '\n'
    row = ['config.yaml']+[c.replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['Common']+[parsed_configs[c]['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['MOM']+[parsed_configs[c]['submodels-by-name']['ocean']['input'] for c in configs]
    row = [r',\quad '.join(x) if isinstance(x, list) else x for x in row]  # deal with list
    row = [x.replace('/', '\\slash ') for x in row]
    f.write(rowstr.format(*row))
    row = ['CICE']+[parsed_configs[c]['submodels-by-name']['ice']['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['YATM']+[parsed_configs[c]['submodels-by-name']['atmosphere']['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    f.write('\\hline\n\\end{tabularx}')

print('Done.')
