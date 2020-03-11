# for using under interactive mode:
# Script for plotting d20 for different resoluvations of access-om2 model and comaparing with woa13

# Steps to produce final figure:
# 1) Extract  data for Indian Ocean for all configurations during time period 1985-2013 (conservative temperature)
# 2) Calculated D20 in Ferret
# 3) observation used from cosima/woa13/10
# 4)  Used python to generate final figure (this script).​


#======================Steps for olading required python libraries==================================
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import datetime
from matplotlib.ticker import NullFormatter

# Steps reading experiments and path for input and output--------------------------------
#/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/woa13_d20_access_om2_grid.nc
exp1 = '1deg_jra55v13_iaf_spinup1_B1' # 1deg
exp2 = '025deg_jra55v13_iaf_gmredi6'  #025 degree
exp3 = '01deg_jra55v13_iaf'           #01 degree
exp4 = 'woa13'
outputdir1 = '/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/python/'
inputdir1 = '/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/1/'
inputdir2 = '/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/025/'
inputdir3 = '/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/01/'
inputdir4 = '/g/data/hh5/tmp/as7904/access-om2/postprocessing/data_files/Indian_ocean/'

#Reading variables and stroring in a list through loop------------------------------------------------------
def plot_fig3(exp1,input1,exp2,input2,exp3,input3,exp4,input4):

        filename = [input1 + exp1 + '_ocean_month_1985_2013_d20_cli.cdf',input2 + exp2 + '_ocean_month_1985_2013_d20_cli.cdf',input3 + exp3 +\
		'_ocean_month_1985_2013_d20_cli.cdf', input4 + exp4 + '_d20_access_om2_grid.nc']

        f_index = 0
        for ff in (filename):
                f_index = f_index + 1
                print(f_index)
                ncfile = Dataset(ff)
                # read variables
		if f_index==4:
                        print('if ==4 case')
			d20_tmp =ncfile.variables['D20_WOA13'][:]
		else:
			print('else case')
			d20_tmp = ncfile.variables['D20_CLI'][:]

#Reading lat and lon for each experiments----------------------------------------------------------------------
                if f_index == 1 :
                        Xlon1 = ncfile.variables['XT_OCEAN301_420'][:]
                        Ylat1 = ncfile.variables['YT_OCEAN78_197'][:]
		elif f_index == 2:
			Xlon2 = ncfile.variables['XT_OCEAN1201_1680'][:]
                        Ylat2 = ncfile.variables['YT_OCEAN373_624'][:]
		elif f_index == 3:
                        Xlon3 = ncfile.variables['XT_OCEAN3001_4201'][:]
                        Ylat3 = ncfile.variables['YT_OCEAN931_1560'][:]
		elif f_index == 4:
                        Xlon4 = ncfile.variables['GRID_X_T301_410'][:]
                        Ylat4 = ncfile.variables['GRID_Y_T78_208'][:]
                ncfile.close()
# printing dimension of the variable
		print('D20 var size =', d20_tmp.shape)
# assign temp var to array and calculating mean with time (0) and removing the dimension by using squeeze-----------------------------
                if f_index == 1 :
                        d20_1 = np.squeeze(np.nanmean(d20_tmp,axis=0))
                elif f_index == 2:
                        d20_2 = np.squeeze(np.nanmean(d20_tmp,axis=0))
		elif f_index == 3:
                        d20_3 = np.squeeze(np.nanmean(d20_tmp,axis=0))
		elif f_index == 4:
                        d20_4 = np.squeeze(np.nanmean(d20_tmp,axis=0))
                del d20_tmp
       		#print('Sizes d20_1, d20_2, Xlon1, Ylat1 Xlon2, Ylat2 = ', d20_1.shape, d20_2.shape, Xlon1.shape, Ylat1.shape, Xlon1.shape, Ylat1.shape)
# Creating mesh grid for each experiment-----------------------------------------------------------------------------------------------
        Y1, X1 = np.meshgrid(Ylat1, Xlon1, sparse=False, indexing='ij')
        print('Sizes X1, Y1 = ', X1.shape, Y1.shape)
	
	Y2, X2 = np.meshgrid(Ylat2, Xlon2, sparse=False, indexing='ij')
        print('Sizes X2, Y2 = ', X2.shape, Y2.shape)
	
        Y3, X3 = np.meshgrid(Ylat3, Xlon3, sparse=False, indexing='ij')
	print('Sizes X3, Y3 = ', X3.shape, Y3.shape)

        Y4, X4 = np.meshgrid(Ylat4, Xlon4, sparse=False, indexing='ij')
        print('Sizes X4, Y4 = ', X4.shape, Y4.shape)

        # plot
        fig = plt.figure(figsize=(12,8))     #(16,8))
#====================================================ACCESS-OM2 =================================================================
        ax = fig.add_subplot(221)
        ax.set_title('a) ACCESS-OM2',fontsize=18)
        # basemap
        #m = Basemap(projection='cyl',llcrnrlat=Y1.min(),urcrnrlat=Y1.max(),llcrnrlon=X1.min(),urcrnrlon=X1.max(),resolution='c',ax=ax)
        #x, y = m(X1,Y1)
        m = Basemap(projection='cyl',llcrnrlat=-30,urcrnrlat=30,llcrnrlon=30,urcrnrlon=120,resolution='c',ax=ax)
        x, y = m(X1,Y1)

        #cs = m.pcolormesh(X1,Y1,d20_1,shading='flat',cmap=plt.cm.PiYG,latlon=True,vmin=40., vmax=200.,ax=ax)
        cs = m.pcolormesh(X1,Y1,d20_1,shading='flat',cmap=plt.cm.rainbow,latlon=True,vmin=40., vmax=200.)
#	fig.colorbar(cs, extend='both')
        m.drawcoastlines(linewidth=0.15)
        m.fillcontinents(color='gray',lake_color='aqua')
        # draw parallels and meridians.
        parallels = np.arange(-30.,30,10.)
	#arallels = np.arange(-30.,91,30.)
        # labels = [left,right,top,bottom]
        m.drawparallels(parallels,labels=[True,False,True,False])
        meridians = np.arange(30.,120.,20.)
        m.drawmeridians(meridians,labels=[True,False,False,True])
        #plt.xlabel('longitude')
        #plt.ylabel('latitude')

        #plt.colorbar(cs, shrink=0.7)
        plt.margins(tight=True)
#Steps for ploting SD ridge box region-----------------------------------------------------------------------------------------------------------
	m.drawgreatcircle(50,-10,75,-10,linewidth=2,color='k')
	m.drawgreatcircle(75,-10,75,-5,linewidth=2,color='k')
        m.drawgreatcircle(75,-5,50,-5,linewidth=2,color='k')
        m.drawgreatcircle(50,-5,50,-10,linewidth=2,color='k')
	m.drawcoastlines()
	m.fillcontinents()
       # plt.savefig(outputdir1 + 'access-om2-1deg_jra-ryf_compar_CORE1_fig3.png')
#=========================================================================== ACCESS-OM2-025=======================================================
	ax = fig.add_subplot(222)
        ax.set_title('b) ACCESS-OM-025',fontsize=18)
        # basemap
        m = Basemap(projection='cyl',llcrnrlat=-30,urcrnrlat=30,llcrnrlon=30,urcrnrlon=120,resolution='c',ax=ax)
        x, y = m(X2,Y2)
        cs = m.pcolormesh(X2,Y2,d20_2,shading='flat',cmap=plt.cm.rainbow,latlon=True,vmin=40., vmax=200.)
        m.drawcoastlines(linewidth=0.15)
        m.fillcontinents(color='gray',lake_color='aqua')
        # draw parallels and meridians.
        parallels = np.arange(-30.,30,10.)
        # labels = [left,right,top,bottom]
        m.drawparallels(parallels,labels=[True,False,True,False])
        meridians = np.arange(30.,120.,20.)
        m.drawmeridians(meridians,labels=[True,False,False,True])
        #plt.xlabel('longitude')
        #plt.ylabel('latitude')
        #plt.colorbar(cs, shrink=0.7)
	#fig.colorbar(cs, extend='both')
        #plt.margins(tight=True)
#Steps for ploting SD ridge  region-----------------------------------------------------------------------------------------------------------------
        m.drawgreatcircle(50,-10,75,-10,linewidth=2,color='k')
        m.drawgreatcircle(75,-10,75,-5,linewidth=2,color='k')
        m.drawgreatcircle(75,-5,50,-5,linewidth=2,color='k')
        m.drawgreatcircle(50,-5,50,-10,linewidth=2,color='k')
	m.drawcoastlines()
        m.fillcontinents()        
#plt.show()
        #plt.savefig(outputdir1 + 'access-om2-1deg_jra-ryf_compar_CORE1_fig3.png
#========================================================access-om-01===================================================================================== 
 	ax = fig.add_subplot(223)
        ax.set_title('c) ACCESS-OM2-01',fontsize=18)
        # basemap
        m = Basemap(projection='cyl',llcrnrlat=-30,urcrnrlat=30,llcrnrlon=30,urcrnrlon=120,resolution='c',ax=ax)
        x, y = m(X3,Y3)
        cs = m.pcolormesh(X3,Y3,d20_3,shading='flat',cmap=plt.cm.rainbow,latlon=True,vmin=40., vmax=200.)
        m.drawcoastlines(linewidth=0.15)
        m.fillcontinents(color='gray',lake_color='aqua')
        # draw parallels and meridians.
        parallels = np.arange(-30.,30,10.)
        # labels = [left,right,top,bottom]
        m.drawparallels(parallels,labels=[True,False,True,False])
        meridians = np.arange(30.,120.,20.)
        m.drawmeridians(meridians,labels=[True,False,False,True])
       # plt.xlabel('longitude')
       # plt.ylabel('latitude')
#	fig.colorbar(cs, extend='both')
        #plt.colorbar(cs, shrink=0.7)
        plt.margins(tight=True)
#Steps for ploting SD ridge  region-------------------------------------------------------------------------------------------------------------------
        m.drawgreatcircle(50,-10,75,-10,linewidth=2,color='k')
        m.drawgreatcircle(75,-10,75,-5,linewidth=2,color='k')
        m.drawgreatcircle(75,-5,50,-5,linewidth=2,color='k')
        m.drawgreatcircle(50,-5,50,-10,linewidth=2,color='k')
	m.drawcoastlines()
        m.fillcontinents()
#=========================================================Observed from WOA13=======================================================================
	ax = fig.add_subplot(224)
        ax.set_title('d) WOA13',fontsize=18)
        # basemap
        m = Basemap(projection='cyl',llcrnrlat=-30,urcrnrlat=30,llcrnrlon=30,urcrnrlon=120,resolution='c',ax=ax)
        x, y = m(X4,Y4)

        cs = m.pcolormesh(X4,Y4,d20_4,shading='flat',cmap=plt.cm.rainbow,latlon=True,vmin=40., vmax=200.)

        m.drawcoastlines(linewidth=0.15)
        m.fillcontinents(color='gray',lake_color='aqua')
        # draw parallels and meridians.
        parallels = np.arange(-30.,30,10.)
        # labels = [left,right,top,bottom]
        m.drawparallels(parallels,labels=[True,False,True,False])
        meridians = np.arange(30.,120.,20.)
        m.drawmeridians(meridians,labels=[True,False,False,True])
        #plt.xlabel('longitude')
        #plt.ylabel('latitude')

        #plt.colorbar(cs, shrink=0.7)
        plt.margins(tight=True)
        #fig.colorbar(cs, extend='both')
#Steps for ploting SD ridge region-------------------------------------------------------------------------------------------------------------------
        m.drawgreatcircle(50,-10,75,-10,linewidth=2,color='k')
        m.drawgreatcircle(75,-10,75,-5,linewidth=2,color='k')
        m.drawgreatcircle(75,-5,50,-5,linewidth=2,color='k')
        m.drawgreatcircle(50,-5,50,-10,linewidth=2,color='k')
	m.drawcoastlines()
        m.fillcontinents()
	cbar_ax = fig.add_axes([.91, 0.2, 0.01, 0.6]) # (xstart,ystart,xend,yend)
	fig.colorbar(cs, cax=cbar_ax,extend='both')
	#plt.legend(loc='upper right')
	plt.ylabel('Depth (m)',fontsize=12)
#Step for saving figure in .png format==========================================================
        plt.savefig(outputdir1 + 'access_om2_all_resoluvations_woa13__d20_isotherm_annal_mean_cosima_paper_2019.png')

# final function
##
plot_fig3(exp1,inputdir1,exp2,inputdir2,exp3,inputdir3,exp4,inputdir4)
