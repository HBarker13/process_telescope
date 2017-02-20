#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Use the master flat in each filter to de-flatten each of the science images"""

import glob
from astropy.io import fits
import numpy as np
import os
import sys
from shutil import copyfile



data_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/Sorted'
master_flat_dir = data_dir + '/master_flats'
night_dirs = glob.glob(data_dir+'/Night*')

#list of all the master flat files
master_fpaths = glob.glob(master_flat_dir+'/*.fits')



#read in all the master flats: fasters than looping over all the exposures, opening them
#and checking they have the correct filter

for master_flat in master_fpaths:

	#find the filter of the master flat
	_, filtername = master_flat.rsplit('masterflat_')
	filtername = filtername[:-5] #remove '.fits'

	master = fits.open(master_flat)
	master_arr = np.array(master[0].data)
	master.close()
	
	if filtername=='U': master_u = master_arr
	elif filtername=='B': master_b = master_arr
	elif filtername=='V': master_v = master_arr
	elif filtername=='R': master_r = master_arr
	
#use the Night1 + Night3 I band flat
master = fits.open( master_flat_dir + '/masterflat_I.fits')
master_i = master[0].data
master.close()
		
	
	

#loop though nights
for night in night_dirs:
	
	obj_dirs = [line for line in glob.glob(night+'/*') if 'Bias' not in line and 'Flat' not in line]
		
	#choose a directory/object
	for obj in obj_dirs:
		
		#list overscan corrected, debiased files
		exposures = glob.glob(obj+'/*ovscorr_debiased.fits')
			
		for fpath in exposures:
			
			#copy the file into the deflattened filename
			savepath = fpath[:-5] + '_deflat.py'
			
			#skip if the deflattened file already exists
			#if os.path.exists(savepath):
			#	continue
			
			copyfile(fpath, savepath)
			
			#open the copy and find out the filter
			exposure = fits.open(savepath, mode='update')
			hdr = exposure[0].header
			img = np.array(exposure[0].data)
			
					
			
			#NEED TO CHECK THE OBSERVING NOTES FOR ANY EXCEPTIONS
			
			#all data seems to be in header['object']: name_filter_exptime
			try:				
				name, filtername, exptime = hdr['object'].split('_')
			except:
				print 'Broken header'
				for line in hdr:
					print line, hdr[line]
				raw_input('')
				print fpath
				sys.exit()

	
			#divide the image by the master flat
			if filtername == 'U': flat = master_u
			if filtername == 'B': flat = master_b
			if filtername == 'V': flat = master_v
			if filtername == 'R': flat = master_r
			if filtername == 'I': flat = master_i



			#check the master flat and image are the same size:
			if np.shape(flat) != np.shape(img):
				print 'Master flat does not have the same dimensions as the img'
				print 'Master flat: ', len(flat[0]), len(flat[1])
				print fpath
				print len(img[0]), len(img[1])
				sys.exit()
				
				
			#divide the img by the masterflat
			deflattened = np.divide(img, flat)
			
			#save the image
			exposure[0].data = deflattened	

			#add a header flag
			hdr.append( ('DEFLAT', 'True', 'De-flattened'), end=True )
			
			
			#save the changes
			exposure.flush()
			exposure.close()
			print 'Created: ', savepath
			print
				
				
			#delete the old file
			os.remove(fpath)	
			
			
			
			
			
			
			
			
			
			
			
			
			
