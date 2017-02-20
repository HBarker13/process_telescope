#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Create master flats for each filter on each night"""

import glob
from astropy.io import fits
import numpy as np
import os
import sys
from shutil import copyfile

data_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/Sorted'


"""There aren't flats for every night. I've kept the flats in directories according to the night they were made to avoid more confusion with the filters used on Night 1. I have kept the same labelling as was used in the observing log (ie. with the incorrect filter names.) The corrections are:
	U -> V
	B -> R
	V -> I
	R -> RG delta50 ?
	I -> Bessel z
I have deviated from the wording on the observing log and named all the flatfields 'flat', rather than 'sky'
"""

#master flat directory. 
#NB. In this directory, the flats are named correctly, ie. the Night1 flats have been labelled 
#using the filter ~really used, not the one recorded in the observing notes
master_dir = data_dir + '/master_flats'
if not os.path.exists(master_dir):
	os.makedirs(master_dir)



#loop through each night
for nightnum in range(1,4):
	print 'Night', nightnum
	night_dir = data_dir + '/Night'+str(nightnum)
	
	flat_dirs = [line for line in glob.glob(night_dir+'/*') if 'Flat_' in line]
	

	#loop through each directory containing flat files
	for flat_dir in flat_dirs:
			
		#get the filter, remembering the changes for Night1
		_, filtername = flat_dir.rsplit('Flat_')
		if nightnum==1:
			if filtername=='U': filtername = 'V'
			elif filtername=='B': filtername = 'R'
			elif filtername=='V': filtername = 'I'
			elif filtername=='R': filtername = 'RGdelta50'
			elif filtername=='I': filtername = 'Bezzel_z'
		
		print 'Filter', filtername
		
		#filename the master flat will be saved to
		savepath = master_dir + '/Night'+str(nightnum) + '_masterflat_' + filtername+'.fits'
		
		#if os.path.exists(savepath):
		#	continue
			 
		
		#start with an empty flat array, and sum the arrays in each flat file
		summed_flat = []
		
		#use overscan corrected, debiased flat frames
		flat_fpaths = glob.glob(flat_dir+'/*ovscorr_debiased.fits')
		if len(flat_fpaths)==0:
			print 'No overscan corrected, debiased flat files found'
			print 'Try overscan_correct.py, debias.py'
			import sys
			sys.exit()
			
		counter = 0
		for flat in flat_fpaths:
			open_flat = fits.open(flat)
			flat_data = open_flat[0].data
			open_flat.close()
		
			#sum the flat arrays
			if len(summed_flat)==0:
				summed_flat = flat_data
				
			else:
				summed_flat = np.add(summed_flat, flat_data)
				
			counter+=1
			
		#divide the calculated master_bias array by the total number of biases
		#ie. calculate the mean for each pixel
		master_flat = np.divide( np.array(summed_flat), counter)
			
		
		#save the master flat
		hdu = fits.PrimaryHDU(master_flat)
		hdu.writeto(savepath)
		print 'Saved: ', savepath	
		
		
	print	






























