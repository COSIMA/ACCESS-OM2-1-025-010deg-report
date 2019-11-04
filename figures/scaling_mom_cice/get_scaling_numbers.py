 # coding: utf-8

from collections import defaultdict
import itertools as it
import os
import sys

import numpy as np
import yaml
import csv

resolutions = ('1', '025', '01')
fname = {
    'ocn': 'deg',
    'ice_step': 'cice'
}

pelist = []
runtimes = {}

ompi_runtimes_all = dict()

for tname in ('ocn','ice_step'):
    for res in resolutions:
        timings_fname = 'timings_{}{}.yaml'.format(res, fname[tname])
        print(timings_fname)

        # Open runtimes
        with open(timings_fname, 'r') as timings_file:
            timings = yaml.load(timings_file)

        ompi_runtimes = []
        for expt in timings:
            for run in timings[expt]:
                if tname is 'ocn':
                    steps = timings[expt][run]['steps']
                    npes = timings[expt][run]['npes']
                    time = timings[expt][run]['runtimes'][tname]
                    ompi_runtimes.append((npes, time / steps))
                else:
                    npes = timings[expt][run]['ice_npes']
                    tmean = timings[expt][run]['runtimes'][tname]['mean']
                    tmax = timings[expt][run]['runtimes'][tname]['max']
                    tsteps = timings[expt][run]['runtimes'][tname]['count']

                    # "Correct" the timing by removing the largest value, which
                    # is attributed to a one-time I/O event.
                    runtime = ((tmean * tsteps - tmax) / (tsteps - 1))
                    ompi_runtimes.append((npes, runtime))
        ompi_runtimes_all[timings_fname] = ompi_runtimes
        pelist.extend([pt[0] for pt in ompi_runtimes])

ompi_runtimes_means = dict()
for timings_fname, timings in ompi_runtimes_all.items():
    cores = list(set([r[0] for r in timings]))
    cores.sort()
    means = list()
    for c in cores:
        means.append(np.mean([r[1] for r in timings if r[0] == c]))
    ompi_runtimes_means[timings_fname] = list(zip(cores, means))

for timings_fname, timings in ompi_runtimes_all.items():
    outfile = os.path.splitext(timings_fname)[0] + '.csv'
    print('\nWriting', outfile)
    with open(outfile, 'w', newline='') as csvfile:
        csvw = csv.writer(csvfile, dialect='excel')
        csvw.writerow(['Cores', 'Mean walltime per step (s)', 'Mean CPU hr per step'])
        for d in ompi_runtimes_means[timings_fname]:
            csvw.writerow([d[0], d[1], d[0]*d[1]/3600])
    print('Done.')
