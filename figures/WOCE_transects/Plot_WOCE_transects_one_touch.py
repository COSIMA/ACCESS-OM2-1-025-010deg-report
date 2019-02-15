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
transect_name_list = ['SR1','SR3','P16','A16','I08-09']
transect_lons_list = [-65,140,-150,-25,95]
transect_lat_limits_list = [[-65,-55],[-70,-42],[-80,80],[-80,80],[-80,20]]
MIN_TEMPERATURE          = [-2,-2,-5,-5,-5]
MAX_TEMPERATURE          = [7 ,12,30,30,30]


#==========================================================================#
#Set labels and the cycle lengths for the individual experiments 
#==========================================================================#

labels  = ['(a) ACCESS-OM2',r'(b) ACCESS-OM2-025','(c) ACCESS-OM2-01', '(d) Observations']
IAF_CYCLE_LENGTH         = [-25*12,25,25]

output_figure_path = './'


MAX_DEPTH = 4500

experiments = ['1deg_jra55v13_iaf_spinup1_B1','025deg_jra55v13_iaf_gmredi6','01deg_jra55v13_iaf']
#experiments = [ '1deg_jra55v13_iaf_spinup1_A','1deg_jra55v13_iaf_spinup1_A','1deg_jra55v13_iaf_spinup1_A']



observations_path     = '/home/157/amh157/v45/amh157/COSIMA_Paper'
observation_file_name = 'WOA13_temperature_salinity_1985_2013_remap.nc'



temperature_transect = []
salt_transect        = [] 

MAX_LON_MODEL =   79.5
MIN_LON_MODEL = -279.5




xticks = np.arange(-80,80.1,10)
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

    fig = plt.figure(1,figsize=(20,10))
    counter  = 1
    for i_exp in range(0,len(experiments)):

        print('Experiment : ', experiments[i_exp])
        start_index = -IAF_CYCLE_LENGTH[i_exp]
        temperature = cosima_cookbook.get_nc_variable(experiments[i_exp],'ocean.nc','temp',chunks={'time':1,'xt_ocean':5},n=start_index)
        temperature = temperature.sel(xt_ocean=transect_lon,method='nearest').mean('time') + KELVIN_TO_CELSIUS

        if PLOT_BIAS:
      
            temperature_obs_on_model_grid = temperature_transect_obs.interp_like(temperature)
       
            temperature = temperature - temperature_obs_on_model_grid
            color_bar_limits = [MIN_TEMP_BIAS,MAX_TEMP_BIAS]
            colormap         = cmocean.cm.balance
            cbar_label       = r'Temperature Bias ($^{\circ}$C)'
        else:
            color_bar_limits = [MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect]]
            colormap         = cmocean.cm.thermal
            cbar_label       = r'Temperature ($^{\circ}$C)'
        ax = fig.add_subplot(2,2,counter)
        cs_temp = ax.contourf(temperature['yt_ocean'],-temperature['st_ocean'],temperature,np.linspace(color_bar_limits[0],color_bar_limits[1],20),cmap=colormap,extend='both')

        #=================================# 
        #Set up the axes ticks and labels
        #=================================# 
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_xlim(transect_lat_limits_list[i_transect])
        if counter == 3:
            ax.set_xlabel("Latitude",fontsize=15)
 
        ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
        ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
        ax.set_ylim([-MAX_DEPTH,0])
        if counter ==1 or counter==3:
            ax.set_ylabel(r"Depth (m)",fontsize=15) 
        #=================================# 
        #Colorbar
        #=================================# 
        if counter == 2:
            n_colorbar_ticks = 10
            cbar = fig.colorbar(cs_temp,ax=ax,ticks=np.linspace(color_bar_limits[0],color_bar_limits[1],n_colorbar_ticks))
            cbar.set_label(cbar_label,fontsize=20)

        #=================================#
        #Annotation
        #=================================#
        ax.annotate(labels[i_exp],
            xy=(0.5, 1.05), xycoords='axes fraction',
            horizontalalignment='center', verticalalignment='bottom',fontsize=15,color='black')
        counter = counter + 1


    ax = fig.add_subplot(2,2,counter)
    cs_temp = ax.contourf(temperature_transect_obs['yt_ocean'],-temperature_transect_obs['st_ocean'],temperature_transect_obs,np.linspace(MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect],20),cmap=cmocean.cm.thermal,extend='both')
    n_colorbar_ticks = 10
    cbar = fig.colorbar(cs_temp,ax=ax,ticks=np.linspace(MIN_TEMPERATURE[i_transect],MAX_TEMPERATURE[i_transect],n_colorbar_ticks))
    cbar.set_label('Temperature ($^{\circ}C$)',fontsize=20)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlim(transect_lat_limits_list[i_transect])
    ax.set_xlabel("Latitude",fontsize=15)

    ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
    ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
    ax.set_ylim([-MAX_DEPTH,0])

    #=================================# 
    # Annotations
    #=================================# 
    ax.annotate(labels[3],
            xy=(0.5, 1.05), xycoords='axes fraction',
            horizontalalignment='center', verticalalignment='bottom',fontsize=15,color='black')

    output_figure_path = './'
    figure_file_name   = 'Model_vs_WOA13_Temperature_' + transect_name

    if PLOT_BIAS:
        figure_file_name = figure_file_name + '_bias'
    plt.savefig(output_figure_path + figure_file_name + '.pdf', dpi=150)
    plt.savefig(output_figure_path + figure_file_name + '.png', dpi=150)
#    plt.savefig(output_figure_path + figure_file_name + '.eps', dpi=150)
    plt.close('all')

    #===============================================#
    # Plot Salinity Sections
    #===============================================#

    fig = plt.figure(2,figsize=(20,10))
    counter  = 1
    for i_exp in range(0,len(experiments)):

        print('Experiment : ', experiments[i_exp])
        start_index = -IAF_CYCLE_LENGTH[i_exp]

        salt  = cosima_cookbook.get_nc_variable(experiments[i_exp],'ocean.nc','salt',chunks={'time':1,'xt_ocean':5},n=start_index)
        salt  = salt.sel(xt_ocean=transect_lon,method='nearest') .mean('time')
        
        if PLOT_BIAS:
      
            salt_obs_on_model_grid        = salt_transect_obs.interp_like(salt)
            salt                          = salt - salt_obs_on_model_grid
            color_bar_limits = [MIN_SALT_BIAS,MAX_SALT_BIAS]
            colormap         = cmocean.cm.balance
            cbar_label       = r'Salinity Bias (psu)'
        else:
            color_bar_limits = [MIN_SALT,MAX_SALT]
            colormap         = cmocean.cm.haline
            cbar_label       = r'Salinity (psu)'

        ax = fig.add_subplot(2,2,counter)
        cs_salt = ax.contourf(salt['yt_ocean'],-salt['st_ocean'],salt,np.linspace(color_bar_limits[0],color_bar_limits[1],20),cmap=colormap,extend='both')

        #=================================# 
        # Set up the axes ticks and labels
        #=================================# 
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_xlim(transect_lat_limits_list[i_transect])
        if counter == 3:
            ax.set_xlabel("Latitude",fontsize=15)
 
        ax.set_yticks(np.arange(-MAX_DEPTH,0.1,1000))
        ax.set_yticklabels(np.arange(MAX_DEPTH,0.1,-1000).astype(np.int))
        ax.set_ylim([-MAX_DEPTH,0])
        if counter ==1 or counter==3:
            ax.set_ylabel(r"Depth (m)",fontsize=15) 
        
        #=================================# 
        # Colorbar
        #=================================# 
        if counter == 2:
            n_colorbar_ticks = 10
            cbar = fig.colorbar(cs_salt,ax=ax,ticks=np.linspace(color_bar_limits[0],color_bar_limits[1],n_colorbar_ticks))
            cbar.set_label(cbar_label,fontsize=20)

        #=================================# 
        # Annotations
        #=================================# 
        ax.annotate(labels[i_exp],
            xy=(0.5, 1.05), xycoords='axes fraction',
            horizontalalignment='center', verticalalignment='bottom',fontsize=15,color='black')


        counter = counter + 1
        
    ax = fig.add_subplot(2,2,counter)
    cs_salt = ax.contourf(salt_transect_obs['yt_ocean'],-salt_transect_obs['st_ocean'],salt_transect_obs,np.linspace(MIN_SALT,MAX_SALT,20),cmap=cmocean.cm.haline,extend='both')
    

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_xlim(transect_lat_limits_list[i_transect])
    ax.set_ylim([-MAX_DEPTH,0])
    ax.set_xlabel("Latitude",fontsize=15)

    n_colorbar_ticks = 10
    cbar = fig.colorbar(cs_salt,ax=ax,ticks=np.linspace(MIN_SALT,MAX_SALT,n_colorbar_ticks))
    cbar.set_label('Salinity (psu)',fontsize=20)

    ax.annotate(labels[3],
            xy=(0, 1.05), xycoords='axes fraction',
            horizontalalignment='center', verticalalignment='bottom',fontsize=15,color='black')


    output_figure_path = './'
    figure_file_name   = 'Model_vs_WOA13_Salinity_' + transect_name
    if PLOT_BIAS:
        figure_file_name = figure_file_name + '_bias'

    plt.savefig(output_figure_path + figure_file_name + '.pdf', dpi=150)
    plt.savefig(output_figure_path + figure_file_name + '.png', dpi=150)
#    plt.savefig(output_figure_path + figure_file_name + '.eps', dpi=150)
    plt.close('all')

#    plt.show()     

