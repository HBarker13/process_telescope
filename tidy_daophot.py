#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Remove daophot working files"""


import os
import glob


#remove .ap, .coo, .lst, .nei files
all_fnames = glob.glob(os.getcwd()+'/*')

for name in all_fnames:
	
	if name[-3:]=='.ap':
		os.remove(name)
		
	if name[-4:]=='.coo':
		os.remove(name)
		
	if name[-4:]=='.lst':
		os.remove(name)
		
	if name[-4:]=='.nei':
		os.remove(name)
	
