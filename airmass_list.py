#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

""" Make a .txt file of airmasses and filenames for the standard stars."""

import os
import glob
from astropy.io import fits




data_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/Sorted/'
night_dirs = glob.glob(data_dir+'/Night*')

#loop through the nights
for night in night_dirs:
	
	#list of standard star directories
	standard_dirs = glob.glob(night+'/st*')
	
	for standard in standard_dirs:
		print standard
	
		#filename to save to
		savepath = standard+'/airmasses.tab'
		
		tab = []
		
		#list of processed files
		fpaths = glob.glob(standard+'/*ovscorr_debiased_deflat.fits')
		
		for f in fpaths:
		
			_, filename = f.rsplit('/', 1) 
			
			#open each files and read the airmass
			airmass = fits.getval(f, 'airmass', 0)
			tab.append([filename, airmass])
			
		
		#order table by exposure number
		tab = sorted(tab)
		
		#save the table
		with open(savepath, 'w+') as savefile:
			for line in tab:
				savefile.write(str(line[0])+'	'+str(line[1]))
				savefile.write('\n') #line break
				
		print 'Saved'
		










