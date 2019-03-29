#!/usr/bin/env python

# Automatically update latex tables of namelists etc for latest runs used in figures

import nmltab  # from https://github.com/aekiss/nmltab
import os
import glob
import yaml
import re

# now redundant
# print('Updating table of experiments...')
# os.system('python ../figures/exptdata.py --latex >| ../figures/exptdata.tex')

print('Downloading latest namelists for runs used in figures...')
os.system('./get_namelists.sh')

exec(open('../figures/exptdata.py').read())  # do nmls for runs used in figures

nmls_common = [
    '/accessom2.nml',
    # '/atmosphere/input_atm.nml',  # for MATM: obsolete
    '/atmosphere/atm.nml',  # for YATM
    ]

nmls_mom = [
    '/ocean/input.nml',
    ]

nmls_cice = [
    '/ice/input_ice.nml',
    '/ice/input_ice_gfdl.nml',
    '/ice/input_ice_monin.nml',
    '/ice/cice_in.nml'
    ]

# nmls = [
#     '/accessom2.nml',
#     '/ocean/input.nml',
#     # '/atmosphere/input_atm.nml',  # for MATM: obsolete
#     '/atmosphere/atm.nml',  # for YATM
#     '/ice/input_ice.nml',
#     '/ice/input_ice_gfdl.nml',
#     '/ice/input_ice_monin.nml',
#     '/ice/cice_in.nml'
#     ]

nmls = nmls_common + nmls_mom + nmls_cice

print('Identifying latest runs used in figures...')

for e in exptdict.keys():
    exptdir = exptdict[e]['exptdir']
    outputs = glob.glob('./raijin' + exptdir + '/output*')
    outputs.sort()
    exptdict[e]['latestexptdir'] = outputs[-1]

configs = [exptdict[e]['latestexptdir'] for e in exptdict.keys()]

print('Updating latex tables of namelists for latest runs used in figures...')
for n in nmls:
    texfname = os.path.basename(n).replace('.', '_') + '.tex'
    st = nmltab.strnmldict(nmltab.nmldict([c + n for c in configs]), format='latex')
    with open(texfname, 'w') as f:
        f.write(st)
    print('   {}'.format(texfname))

print('Updating latex tables of namelist differences from other configs...')

configs2 = ['OFAM3/input.ofam3_spinup03.nml', 'OFAM3/input.ofam2017.nml']
configs2.append(exptdict['01deg']['latestexptdir']+'/ocean/input.nml')
texfname = 'OFAM3_input_nml.tex'
st = nmltab.strnmldict(nmltab.nmldiff(nmltab.nmldict(configs2)), format='latex')
with open(texfname, 'w') as f:
    f.write(st)
print('   {}'.format(texfname))

configs3 = ['ACCESS-CM2/input.nml']
configs3.append(exptdict['1deg']['latestexptdir']+'/ocean/input.nml')
texfname = 'ACCESS-CM2_input_nml.tex'
st = nmltab.strnmldict(nmltab.nmldiff(nmltab.nmldict(configs3)), format='latex')
with open(texfname, 'w') as f:
    f.write(st)
print('   {}'.format(texfname))

configs4 = ['ACCESS-CM2/cice_in.nml']
configs4.append(exptdict['1deg']['latestexptdir']+'/ice/cice_in.nml')
texfname = 'ACCESS-CM2_cice_in_nml.tex'
st = nmltab.strnmldict(nmltab.nmldiff(nmltab.nmldict(configs4)), format='latex')
with open(texfname, 'w') as f:
    f.write(st)
print('   {}'.format(texfname))

print('Updating latex tables of namelist differences between profiling configs and latest runs used in figures...')
# NB: only *deg were used for mom profiling and only *cice were used for cice profiling
digits = re.compile('\d+')
for e in exptdict.keys():
    profconfigs = glob.glob('./raijin/short/public/mxw900/home/mxw157/om2bench/'
                            + digits.match(e)[0] + '*/*')
    for n in nmls_common:
        configs5 = [p+n for p in profconfigs] + [exptdict[e]['latestexptdir']+n]
        texfname = os.path.basename(n).replace('.', '_') + '_' + e + '_prof_diff.tex'
        os.system('python nmltab.py --format latex -dpi ' + ' '.join(configs5) + '>| ' + texfname)
        print('   {}'.format(texfname))

    profconfigs = glob.glob('./raijin/short/public/mxw900/home/mxw157/om2bench/'
                            + digits.match(e)[0] + 'deg/*')
    for n in nmls_mom:
        configs5 = [p+n for p in profconfigs] + [exptdict[e]['latestexptdir']+n]
        texfname = os.path.basename(n).replace('.', '_') + '_' + e + '_prof_diff.tex'
        os.system('python nmltab.py --format latex -dpi ' + ' '.join(configs5) + '>| ' + texfname)
        print('   {}'.format(texfname))

    profconfigs = glob.glob('./raijin/short/public/mxw900/home/mxw157/om2bench/'
                            + digits.match(e)[0] + 'cice/*')
    for n in nmls_cice:
        configs5 = [p+n for p in profconfigs] + [exptdict[e]['latestexptdir']+n]
        texfname = os.path.basename(n).replace('.', '_') + '_' + e + '_prof_diff.tex'
        os.system('python nmltab.py --format latex -dpi ' + ' '.join(configs5) + '>| ' + texfname)
        print('   {}'.format(texfname))

print('Updating latex tables of within-run namelist differences for latest runs used in figures...')
for n in nmls:
    for k in exptdict.keys():
        texfname = os.path.basename(n).replace('.', '_') + '_' + k + '_diff.tex'
        os.system('python nmltab.py --format latex -dpi ' + './raijin' + exptdict[k]['exptdir'] + '/output*' + n + '>| ' + texfname)
        print('   {}'.format(texfname))

print('Making table of configurations...')
parsed_configs = dict()
for c in configs:
    with open(c + '/config.yaml', 'r') as infile:
        parsed_configs[c] = yaml.load(infile)
    parsed_configs[c]['submodels-by-name'] = dict()
    for sm in parsed_configs[c]['submodels']:
        parsed_configs[c]['submodels-by-name'][sm['name']] = sm
with open('configurations.tex', 'w') as f:
    f.write('% File generated by make_tables.py  --  DO NOT EDIT\n')
    f.write(r'\begin{tabularx}{\linewidth}{p{0.11\linewidth}')
    f.write(r'p{0.26\linewidth}'*len(configs))
    f.write('}\n\\hline\n & \\textbf{')
    f.write(r'} & \textbf{'.join(descs))
    f.write(r'}\\' + '\n\\hline\n')
    rowstr = '{} & ' + r'{{\footnotesize\textsf{{{}}}}} & '*(len(configs)-1) + r'{{\footnotesize\textsf{{{}}}}}\\' + '\n'
    # row = ['config.yaml']+[c.replace('/', '\\slash ') for c in configs]
    # f.write(rowstr.format(*row))
    row = ['Experiment']+expts
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    f.write('MOM' + ' & '*len(configs) + r'\\' + '\n')
    row = ['source']+[r'\url{https://github.com/mom-ocean/MOM5/tree/'+parsed_configs[c]['submodels-by-name']['ocean']['exe'].split('.')[-2].split('_')[-1]+'}' for c in configs]
    f.write(rowstr.format(*row))
    row = ['executable']+[parsed_configs[c]['submodels-by-name']['ocean']['exe'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['inputs']+[parsed_configs[c]['submodels-by-name']['ocean']['input'] for c in configs]
    row = [r',\quad '.join(x) if isinstance(x, list) else x for x in row]  # deal with list
    row = [x.replace('/', '\\slash ') for x in row]
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    f.write('CICE' + ' & '*len(configs) + r'\\' + '\n')
    row = ['source']+[r'\url{https://github.com/OceansAus/cice5/tree/'+parsed_configs[c]['submodels-by-name']['ice']['exe'].split('.')[-2].split('_')[-1]+'}' for c in configs]
    f.write(rowstr.format(*row))
    row = ['executable']+[parsed_configs[c]['submodels-by-name']['ice']['exe'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['inputs']+[parsed_configs[c]['submodels-by-name']['ice']['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    f.write('YATM' + ' & '*len(configs) + r'\\' + '\n')
    row = ['source']+[r'\url{https://github.com/OceansAus/libaccessom2/tree/'+parsed_configs[c]['submodels-by-name']['atmosphere']['exe'].split('.')[-2].split('_')[-1]+'}' for c in configs]
    f.write(rowstr.format(*row))
    row = ['executable']+[parsed_configs[c]['submodels-by-name']['atmosphere']['exe'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    row = ['inputs']+[parsed_configs[c]['submodels-by-name']['atmosphere']['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    row = ['common inputs']+[parsed_configs[c]['input'].replace('/', '\\slash ') for c in configs]
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    row = ['outputs']+[c.replace('/', '\\slash ') for c in exptdirs]
    f.write(rowstr.format(*row))
    f.write('\\hline\n')
    row = [r'run \mbox{summary}']+['/g/data/hh5/tmp/cosima/access-om2-run-summaries/run_summary_'+c+'.csv' for c in expts]
    row = [x.replace('/', '\\slash ') for x in row]
    f.write(rowstr.format(*row))
    f.write('\\hline\n\\end{tabularx}')

print('Done.')
