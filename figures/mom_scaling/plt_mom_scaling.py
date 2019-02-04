# coding: utf-8

from collections import defaultdict
import itertools as it
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import yaml

formats = ('png', 'pdf')
ctxt = 'k'

resolutions = ('1', '025', '01')

p_ref_table = {
    '1': 216,
    '025': 1455,
    '01': 4358,
}

res_color_table = {
    '1': 'g',
    '025': 'orange',
    '01': 'b',
}


for tname in ('ocn',):
    pelist = []
    runtimes = {}
    handles = []

    ax_grid = plt.GridSpec(len(resolutions), 2)
    ax_grid.update(right=1.2, wspace=0.25)
    ax_rt = plt.subplot(ax_grid[:, 0])

    ax_cpus = [plt.subplot(ax_grid[0, 1])]
    ax_cpus.extend(plt.subplot(ax_grid[i, 1], sharex=ax_cpus[0])
                   for i in range(1, len(resolutions)))

    for res in resolutions:
        timings_fname = 'timings_{}deg.yaml'.format(res)
        print(timings_fname)
    
        # Open MPI runtimes
        with open(timings_fname, 'r') as timings_file:
            timings = yaml.load(timings_file)

        ompi_runtimes = []
        for expt in timings:
            for run in timings[expt]:
                steps = timings[expt][run]['steps']
                npes = timings[expt][run]['npes']
                time = timings[expt][run]['runtimes'][tname]
                ompi_runtimes.append((npes, time / steps))

        pelist.extend([pt[0] for pt in ompi_runtimes])

        # Plot theoretical speedup
        pes = np.array(sorted(list(set(pt[0] for pt in ompi_runtimes))))

        p_ref = p_ref_table[res]
        t_ref = np.mean([pt[1] for pt in ompi_runtimes if pt[0] == p_ref])
        t_min = np.min([pt[1] for pt in ompi_runtimes if pt[0] == p_ref])
        t_opt = t_ref * p_ref / pes
        if tname not in ('init'):
            ax_rt.plot(pes, t_opt, '-', color='k', linestyle='--')

        # Plot Open MPI speedup
        for pt in ompi_runtimes:
            ompi_handle, = ax_rt.plot(pt[0], pt[1], 'd',
                                      markeredgewidth=0.5,
                                      markeredgecolor='k',
                                      markersize=8,
                                      color=res_color_table[res])
        handles.append(ompi_handle)

        for pt in ompi_runtimes:
            ax = ax_cpus[resolutions[::-1].index(res)]

            cpu_hrs = pt[1] * pt[0] / 3600.
            efficiency = p_ref * t_ref / (pt[0] * pt[1])
            overhead = pt[0] * pt[1] / (p_ref * t_ref)

            metric = cpu_hrs
            ax.plot(pt[0], metric, 'd',
                markeredgewidth=0.5,
                markeredgecolor='k',
                markersize=8,
                color=res_color_table[res]
            )

    # Axis based on exact PEs used (too numerous in this case)
    #peset = sorted(list(set(pelist)))
    #print(peset)

    # Generic axis with (mostly) uniform spacing and near relevant runs
    peset = [60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]

    for ax in (ax_rt, ax_cpus[-1]):
        ax.set_xscale('log')
        ax.set_xlim(50, 20000)
        ax.set_xticks(peset)
        ax.set_xticklabels(peset, rotation=30)
        ax.set_xlabel('# of CPUs')

        ax.minorticks_off()

        ax.xaxis.label.set_color(ctxt)
        ax.yaxis.label.set_color(ctxt)
        ax.title.set_color(ctxt)
        for label in it.chain(ax.get_xticklabels(), ax.get_yticklabels()):
            label.set_color(ctxt)

    for ax in ax_cpus[:-1]:
        plt.setp(ax.get_xticklabels(), visible=False)

    ax_cpus[0].set_ylim(0.8, 1.3)
    ax_cpus[1].set_ylim(0.1, 0.3)
    ax_cpus[2].set_ylim(0.008, 0.03)

    ax_rt.set_ylim(0.05, 10.)
    ax_rt.set_yscale('log')
    ax_rt.set_ylabel('Runtime / step (s)')
    ax_rt.set_title('(a) Main loop runtime')

    ax_cpus[1].set_ylabel(u'CPU × Runtime / step (hr)', labelpad=10)
    ax_cpus[0].set_title('(b) CPU hours')

    ax_rt.legend(handles, [u'1°', u'0.25°', u'0.1°'])

    for fmt in formats:
        plt.savefig('scaling_{}.{}'.format(tname, fmt),
                    facecolor='none', bbox_inches='tight')
