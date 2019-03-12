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
    'ocn': {
        '1': 216,
        '025': 1455,
        '01': 4358,
    },
    'ice_step': {
        '1': 24,
        '025': 361,
        '01': 1600,
    }
}

fname = {
    'ocn': 'deg',
    'ice_step': 'cice'
}

symbol = {
    'ocn': 'd',
    'ice_step': '*'
}

res_color_table = {
    '1': u'#1f77b4',
    '025': u'#ff7f0e',
    '01': u'#2ca02c',
}


pelist = []
runtimes = {}
handles = []

ax_grid = plt.GridSpec(len(resolutions), 4)
ax_grid.update(right=1.2, wspace=0.45)
ax_rt = plt.subplot(ax_grid[:, 0:2])

ax_cpus = [plt.subplot(ax_grid[0, 2])]
ax_cpus.extend(plt.subplot(ax_grid[i, 2], sharex=ax_cpus[0])
               for i in range(1, len(resolutions)))

ax_cpus_cice = [plt.subplot(ax_grid[0, 3])]
ax_cpus_cice.extend(plt.subplot(ax_grid[i, 3], sharex=ax_cpus_cice[0])
               for i in range(1, len(resolutions)))

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

        pelist.extend([pt[0] for pt in ompi_runtimes])

        # Plot theoretical speedup
        pes = np.array(sorted(list(set(pt[0] for pt in ompi_runtimes))))

        p_ref = p_ref_table[tname][res]
        t_ref = np.mean([pt[1] for pt in ompi_runtimes if pt[0] == p_ref])
        t_min = np.min([pt[1] for pt in ompi_runtimes if pt[0] == p_ref])
        t_opt = t_ref * p_ref / pes
        if tname not in ('init'):
            ax_rt.plot(pes, t_opt, '-', color='k', linestyle='--', linewidth=0.5)

        # Plot Open MPI speedup
        for pt in ompi_runtimes:
            ompi_handle, = ax_rt.plot(pt[0], pt[1], symbol[tname],
                                      markeredgewidth=0.5,
                                      markeredgecolor='k',
                                      markersize=8,
                                      color=res_color_table[res])
        handles.append(ompi_handle)

        for pt in ompi_runtimes:
            if tname is 'ocn':
                ax = ax_cpus[resolutions[::-1].index(res)]
            else:
                ax = ax_cpus_cice[resolutions[::-1].index(res)]

            cpu_hrs = pt[1] * pt[0] / 3600.
            efficiency = p_ref * t_ref / (pt[0] * pt[1])
            overhead = pt[0] * pt[1] / (p_ref * t_ref)

            metric = cpu_hrs
            ax.plot(pt[0], metric, symbol[tname],
                markeredgewidth=0.5,
                markeredgecolor='k',
                markersize=8,
                color=res_color_table[res]
            )

    # Generic axis with (mostly) uniform spacing and near relevant runs
    peset = [4, 8, 15, 30, 60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]

    for ax in (ax_rt, ax_cpus[-1], ax_cpus_cice[-1]):
        ax.set_xscale('log')
        ax.set_xlim(4, 20000)
        ax.set_xticks(peset)
        ax.set_xticklabels(peset, rotation=60, fontdict={'fontsize': 8})
        ax.set_xlabel('Number of CPUs')

        ax.minorticks_off()

        ax.xaxis.label.set_color(ctxt)
        ax.yaxis.label.set_color(ctxt)
        ax.title.set_color(ctxt)
        for label in it.chain(ax.get_xticklabels(), ax.get_yticklabels()):
            label.set_color(ctxt)
            # label.set_fontsize(8)

    for ax in ax_cpus[:-1] + ax_cpus_cice[:-1]:
        plt.setp(ax.get_xticklabels(), visible=False)
    for ax in ax_cpus + ax_cpus_cice:
        # print(ax)
        for label in it.chain(ax.get_xticklabels(), ax.get_yticklabels()):
            # label.set_color(ctxt)
            label.set_fontsize(8)
        # label = ax.get_yticklabels()
        # label.set_fontsize(8)
        # plt.setp(ax.get_xticklabels(), visible=False)

    ax_cpus[0].set_ylim(0.8, 1.3)
    ax_cpus[1].set_ylim(0.1, 0.3)
    ax_cpus[2].set_ylim(0.008, 0.03)
    ax_cpus_cice[0].set_ylim(0.15, 0.4)
    ax_cpus_cice[1].set_ylim(0.01, 0.02)
    ax_cpus_cice[2].set_ylim(0.0005, 0.0025)

    ax_rt.set_ylim(0.01, 10.)
    ax_rt.set_yscale('log')
    ax_rt.set_ylabel('Runtime / step (s)')
    ax_rt.set_title('(a) Main loop runtime')

    ax_cpus[1].set_ylabel(u'CPU × Runtime / step (hr)', labelpad=4)
    ax_cpus[0].set_title('(b) MOM CPU hours')
    ax_cpus_cice[0].set_title('(c) CICE CPU hours')

    ax_rt.legend(handles, [u'1° MOM',
                           u'0.25° MOM',
                           u'0.1° MOM',
                           u'1° CICE',
                           u'0.25° CICE',
                           u'0.1° CICE'],
                 fontsize=8)

    for fmt in formats:
        plt.savefig('scaling_{}.{}'.format('mom_cice', fmt),
                    facecolor='none', bbox_inches='tight')
