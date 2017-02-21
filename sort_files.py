#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Sort the data from each night into directories by target name and filter"""


#DON'T USE THIS: TOO MANY HEADERS WERE BROKEN FOR THIS TO WORK RELIABLY

#from pyraf import iraf
import os
import glob
from astropy.io import fits
import numpy as np
from shutil import copyfile



#read in raw files 
data_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/'
nightdirs = glob.glob(data_dir+'/Night*')


#create Sorted directory if it doesn't already exist
sorted_dir = data_dir + '/Sorted'
if not os.path.exists(sorted_dir):
	os.makedirs(sorted_dir)
	
	
#loop through directories of raw files
for night in nightdirs:

	targets = set()	
	#loop though all the files to get the target names
	fpaths = glob.glob(night+'/*.fits')
	for f in fpaths:
		openfile = fits.open(f)
		hdr = openfile[0].header
		obj = hdr['object'] #targetname_filter_exptime
		
		#skip test objects
		if obj =='test': continue
		
		#skip null for now
		if obj =='null': continue
		
		print f
		print obj
		#remove the exposure time
		try:
			objname, _ = obj.rsplit(' ', 1)  #when split with spaces
		except:
			objname, _ = obj.rsplit('_', 1)  #when split with underscores
		
		targets.add( objname ) 
		openfile.close()
		
		
	for t in targets:
		#create directory for each of the targets
		print t
	raw_input('')



