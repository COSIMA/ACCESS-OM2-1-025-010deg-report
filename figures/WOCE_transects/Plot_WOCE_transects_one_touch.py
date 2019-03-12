import logging
logging.captureWarnings(True)
logging.getLogger('py.warnings').setLevel(logging.ERROR)

import matplotlib.pyplot as plt
import xarray
import numpy as np
import cmocean
import cartopy.crs as ccrs
import os
import matplotlib.gridspec as gridspec
import dask
import dask.array as da
import dask.dataframe as dd
from dask import delayed

from dask.distributed import Client
from distributed.diagnostics.progressbar import progress

import cosima_cookbook
KELVIN_TO_CELSIUS = -273.15

PLOT_BIAS = True


MIN_SALT   = 33
MAX_SALT   = 36

if PLOT_BIAS:
    MIN_TEMP_BIAS = -2.0
    MAX_TEMP_BIAS =  2.0

    MIN_SALT_BIAS = -1.0
    MAX_SALT_BIAS =  1.0

#==========================================================================#
#Set up the domain limits, colorbar limits, all that stuff, for the
#individual transects 
#==========================================================================#
transect_name_list = ['SR3','P16','A16','I08-09']                 ##'SR1',
transect_lons_list = [140,-150,-25,95]                            ##-65,
transect_lat_limits_list = [[-67,-42],[-76,61],[-75.01,70],[-65,15.1]] ##[-65,-55],
MIN_TEMPERATURE          = [-2,-2,-2,-2]                          ##-2,
MAX_TEMPERATURE          = [13,28,28,28]                          ##7 ,


#==========================================================================#
#Set labels and the cycle lengths for the individual experiments 
#==========================================================================#

labels  = ['(a) ACCESS-OM2','(b) ACCESS-OM2','(c) ACCESS-OM2-025','(d) ACCESS-OM2-025','(e) ACCESS-OM2-01', '(f) ACCESS-OM2-01','(g) WOA13','(h) WOA13']
IAF_CYCLE_LENGTH         = [12,34,24]  ## FIXME - 3rd entry should be 150!!

output_figure_path = './'


MAX_DEPTH = 4500

experiments = ['1deg_jra55v13_iaf_spinup1_B1','025deg_jra55v13_iaf_gmredi6','01deg_jra55v13_iaf']
#experiments = [ '1deg_jra55v13_iaf_spinup1_A','1deg_jra55v13_iaf_spinup1_A','1deg_jra55v13_iaf_spinup1_A']
Nexp = len(experiments)

observations_path     = '/home/157/amh157/v45/amh157/COSIMA_Paper'
observation_file_name = 'WOA13_temperature_salinity_1985_2013_remap.nc'

temperature_transect = []
salt_transect        = [] 

MAX_LON_MODEL =   79.5
MIN_LON_MODEL = -279.5

xticks = np.arange(-75,75.1,15)
xtick_labels = []
for i_tick in range(xticks.size):
    if xticks[i_tick]<0:
        xtick_labels.append(str(int(abs(xticks[i_tick]))) + r'$^{\circ}$S')
    elif xticks[i_tick]>0:
        xtick_labels.append(str(int(xticks[i_tick])) + r'$^{\circ}$N')
    else:
        xtick_labels.append(str(int(xticks[i_tick])) + r'$^{\circ}$')


for i_transect in range(0,len(transect_name_list)):
    transect_name = transect_name_list[i_transect]
    transect_lon  = transect_lons_list[i_transect]
    print('Plotting transect: ', transect_name_list[i_transect])

    main_label    = r'Transect ' + transect_name + str(transect_lon)

    if transect_lon>MAX_LON_MODEL:
        transect_lon = (transect_lon-MAX_LON_MODEL) + MIN_LON_MODEL  #Model fields go from -280 to 80, so we need to take into accound the shift
        print(transect_lon)
    #END if transect_lon>MAX_LON_MODEL
   
    observation_dataset = xarray.open_dataset(os.path.join(observations_path,observation_file_name),autoclose=False)
    temperature_obs     = observation_dataset['temperature']
    salt_obs            = observation_dataset['salinity']

    temperature_transect_obs = temperature_obs.sel(xt_ocean=transect_lon,method='nearest')
    salt_transect_obs        = salt_obs.sel(xt_ocean=transect_lon,method='nearest')
    
    temperature_transect_obs = temperature_transect_obs.rename({'depth':'st_ocean'})
    salt_transect_obs = salt_transect_obs.rename({'depth':'st_ocean'})
    
    #===============================================#
    # Plot Temperature Sections
    #===============================================#

    fig = plt.figure(1,figsize=(12,12))
    plt.subplots_adjust(bottom=0.14,hspace=0.24)
    
    counter  = 1
    for i_exp in range(0,Nexp):

        print('Experiment : ', experiments[i_exp])
        start_index = -IAF_CYCLE_LENGTH[i_exp]
        temperature = cosima_cookbook.get_nc_variable(experiments[i_exp],'ocean.nc','temp',chunks={'time':1,'xt_ocean':5},n=start_index)
        temperature = temperature.sel(xt_ocean=transect_lon,method='nearest').mean('time') + KELVIN_TO_CELSIUS

        if PLOT_BIAS:
      
            temperature_obs_on_model_grid = temperature_transect_obs.interp_like(temperature)
       
            temperature = temperature - temperature_obs_on_model_grid
            color_bar_limits = [MIN_TEMP_BIAS,MAX_TEMP_BIAS]
            colormap         = cmocean.cm.balance
            cbar_label       = r'Temp Bias ($^{\circ}$C)'
        else:
            color_bar_limits = [MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect]]
            colormap         = cmocean.cm.thermal
            cbar_label       = r'Temperature ($^{\circ}$C)'
        ax = fig.add_subplot(4,2,2*counter-1)
        cs_temp = ax.contourf(temperature['yt_ocean'],-temperature['st_ocean'],temperature,np.linspace(color_bar_limits[0],color_bar_limits[1],20),cmap=colormap,extend='both')

        #=================================# 
        #Set up the axes ticks and labels
        #=================================# 
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_xlim(transect_lat_limits_list[i_transect])
 
        ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
        ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
        ax.set_ylim([-MAX_DEPTH,0])
        ax.set_ylabel(r"Depth (m)") 
        #=================================# 
        #Colorbar
        #=================================# 
        if counter == 2:
            ax1 = plt.axes([0.1,0.08,0.19,0.01])
            n_colorbar_ticks = 5
            cbar = fig.colorbar(cs_temp,cax=ax1,orientation='horizontal',ticks=np.linspace(color_bar_limits[0],color_bar_limits[1],n_colorbar_ticks))
            cbar.set_label(cbar_label)

        #=================================#
        #Annotation
        #=================================#
        ax.set_title(labels[2*i_exp])
        
        counter = counter + 1


    ax = fig.add_subplot(427)
    cs_temp = ax.contourf(temperature_transect_obs['yt_ocean'],-temperature_transect_obs['st_ocean'],temperature_transect_obs,np.linspace(MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect],20),cmap=cmocean.cm.thermal,extend='both')
    ax2 = plt.axes([0.3,0.08,0.19,0.01])
    n_colorbar_ticks = 7
    cbar = fig.colorbar(cs_temp,cax=ax2,orientation='horizontal',ticks=np.linspace(MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect],n_colorbar_ticks))
    cbar.set_label('Temperature ($^{\circ}C$)')

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlim(transect_lat_limits_list[i_transect])
    ax.set_xlabel("Latitude")

    ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
    ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
    ax.set_ylim([-MAX_DEPTH,0])
    ax.set_ylabel(r"Depth (m)")

    #=================================# 
    # Annotations
    #=================================# 
    ax.set_title(labels[6])

    #===============================================#
    # Plot Salinity Sections
    #===============================================#

    counter  = 1
    for i_exp in range(0,Nexp):

        print('Experiment : ', experiments[i_exp])
        start_index = -IAF_CYCLE_LENGTH[i_exp]

        salt  = cosima_cookbook.get_nc_variable(experiments[i_exp],'ocean.nc','salt',chunks={'time':1,'xt_ocean':5},n=start_index)
        salt  = salt.sel(xt_ocean=transect_lon,method='nearest') .mean('time')
        
        if PLOT_BIAS:
      
            salt_obs_on_model_grid        = salt_transect_obs.interp_like(salt)
            salt                          = salt - salt_obs_on_model_grid
            color_bar_limits = [MIN_SALT_BIAS,MAX_SALT_BIAS]
            colormap         = cmocean.cm.balance
            cbar_label       = r'Salt Bias (g/kg)'
        else:
            color_bar_limits = [MIN_SALT,MAX_SALT]
            colormap         = cmocean.cm.haline
            cbar_label       = r'Salinity (g/kg)'

        ax = fig.add_subplot(4,2,2*counter)
        cs_salt = ax.contourf(salt['yt_ocean'],-salt['st_ocean'],salt,np.linspace(color_bar_limits[0],color_bar_limits[1],20),cmap=colormap,extend='both')

        #=================================# 
        # Set up the axes ticks and labels
        #=================================# 
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_xlim(transect_lat_limits_list[i_transect])
 
        ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
        ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
        ax.set_ylim([-MAX_DEPTH,0]) 
        
        ax.set_title(labels[2*i_exp+1])
        
        #=================================# 
        # Colorbar
        #=================================# 
        if counter == 2:
            ax3 = plt.axes([0.53,0.08,0.19,0.01])
            n_colorbar_ticks = 5
            cbar = fig.colorbar(cs_salt,cax=ax3,orientation='horizontal',ticks=np.linspace(color_bar_limits[0],color_bar_limits[1],n_colorbar_ticks))
            cbar.set_label(cbar_label)

        counter = counter + 1
        
    ax = fig.add_subplot(428)
    cs_salt = ax.contourf(salt_transect_obs['yt_ocean'],-salt_transect_obs['st_ocean'],salt_transect_obs,np.linspace(MIN_SALT,MAX_SALT,20),cmap=cmocean.cm.haline,extend='both')
    

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlim(transect_lat_limits_list[i_transect])
    ax.set_ylim([-MAX_DEPTH,0])
    ax.set_xlabel("Latitude")

    ax4 = plt.axes([0.74,0.08,0.19,0.01])
    n_colorbar_ticks = 7
    cbar = fig.colorbar(cs_salt,cax=ax4,orientation='horizontal',ticks=np.linspace(MIN_SALT,MAX_SALT,n_colorbar_ticks))
    cbar.set_label('Salinity (g/kg)')

    ax.set_title(labels[7])


    output_figure_path = './'
    figure_file_name   = 'Model_vs_WOA13_Temp_Salt_' + transect_name
    if PLOT_BIAS:
        figure_file_name = figure_file_name + '_bias'

    #plt.savefig(output_figure_path + figure_file_name + '.pdf', dpi=150)
    plt.savefig(output_figure_path + figure_file_name + '.png', dpi=150)
    
    plt.close('all')

#    plt.show()     

