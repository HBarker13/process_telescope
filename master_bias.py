#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""script to create a master bias frame"""

import os
import glob
from astropy.io import fits
import numpy as np


"""
Notes from observing logs:
	N1 bias taken towards the end of the night
	N2 beginning of the night: 'no sky flats -computer problem'
	N3 bias frames x40 at beginning of night and bias frames 'x20 end of night'
"""

data_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/Sorted/'
night_dirs = glob.glob(data_dir+'/Night*/Bias')

#expected dimensions of the bias arrays
len0 = 2148
len1 = 2148

master_bias = []

for night in night_dirs:
	
	#start with empty array for the bias for each night
	summed_bias = []
	
	#use overscan corrected bias files
	bias_fpaths = glob.glob(night+'/*ovscorr.fits')
	if len(bias_fpaths)==0:
		print 'No overscan corrected files found.'
		print 'Try: overscan_correct.py'
		import sys
		sys.exit()
		
	
	counter = 0
	for bias in bias_fpaths:
		open_bias = fits.open(bias)
		bias_data = open_bias[0].data
		open_bias.close()
		

		#check the bias data has the correct dimensions: 2148 x 2148
		if len(bias_data[0])!=len0 and len(bias_data[1])!=len1:
			print 'Bias data wrong shape'
			print bias
			import sys
			sys.exit()
			
		#sum all the arrays
		if len(summed_bias)==0:
			summed_bias = bias_data
		else:
			#add the master bias and new bias arrays
			summed_bias = np.add(summed_bias, bias_data)
		
		counter+=1


	#divide the calculated master_bias array by the total number of biases
	#ie. calculate the mean for each pixel
	#divisor_arr = np.full( (x_len, y_len), float(counter) )
	master_bias = np.divide( np.array(summed_bias), counter)
	

	#save the master_bias as a new fits file
	savename = night+'/master_bias.fits'
	hdu = fits.PrimaryHDU(master_bias)
	hdu.writeto(savename)
	print 'Saved: ', savename
	print

		
		
		
		
		
		
		
		
		
		
		
			
		
		
		

