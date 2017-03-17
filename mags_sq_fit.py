#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Use a linear least-squares method to calculate observed magntiudes from instrumental magnitudes"""

 
from pyexcel_ods import get_data
import json
import numpy as np
from matplotlib import pyplot as plt 
from scipy.optimize import curve_fit




#read in ods file with standard star magnitudes and airmasses
working_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU'
standard_fpath = working_dir + '/Standard_stars.ods'
all_data = get_data(standard_fpath)


tab = dict()
filternames = ['U', 'B', 'V', 'I']

print 'Reading in data'
for sheetname in all_data:
	
	if sheetname=='Overview':
		continue	

	tab[sheetname] = [] #add name to dictionary
	pn_data = all_data[sheetname]
	
	#skip line[0], contains unnecessary titles
	colnames = pn_data[1]
	pn = pn_data[2:]

	#use measured magnitudes for each repeat
	cols = ['Night', 'Filter', 'Airmass', 'mag', 'mag_err']
	inds = [ i for i,val in enumerate(colnames) if val in cols]

	
	cut_table = []
	blank = False #flag for previous line being blank
	
	for line in pn:
	
		#there are 3 lines between different sets of observations
		if blank==True and len(line)==0: 
			if len(cut_table)>0:
				tab[sheetname].append(cut_table)
			cut_table = []	
			blank=False	
			continue
		
		if len(line)==0: 
			blank = True
			continue #skip empty lines
		
		#skip lines with unwanted filternames
		if line[inds[1]] not in filternames:
			blank = False #resets so the blank lines between unwanted filters aren't counted
			continue	
			
		#skip incomplete lines
		if len(line) < int(inds[4]): continue

		newline = [ line[ind] for ind in inds]		
			
		last_filter = newline[1]
		cut_table.append(newline)
print		
	
		
#pn name: [U, B, V, I ]
true_colours = { 'MCT2019': [12.185, 13.397, 13.685, 13.946], '111-1925':[13.045, 12.783, 12.387, 11.904], 'wd1056':[12.775, 13.86, 14.047, 14.350], 'G93-48':[11.942, 12.732, 12.743, 12.938], 'LSE44':[11.042, 12.194, 12.459, 12.604], '121-968':[9.16, 10.071, 10.256, 10.429]  }	

 
#need to solve the following equations for each filter on each night
#
# B = O_B + b + C_B*(B-V) - KB*Z   
#
# O = instrumental offsets
# C = colour terms
# K = extinction coefficients
# Z = airmass
# B-V is the colour on the standard system


nights = ['Night1', 'Night2', 'Night3']
for night in nights:
	
	#airmass, mag, mag_err, colour, true_mag
	filter_data = []
	
	
	for filtername in filternames:	
		print 'Filter', filtername
		for pn in tab:
			
			if filtername =='U':
				true = true_colours[pn][0]
				colour = true_colours[pn][0] - true_colours[pn][1] #U-B
				
			elif filtername=='B':
				true = true_colours[pn][1]	
				colour = true_colours[pn][1] - true_colours[pn][2] #B-V
				
			elif filtername=='V':
				true = true_colours[pn][2]
				colour = true_colours[pn][1] - true_colours[pn][2] #B-V
				
			elif filtername=='I':
				true = true_colours[pn][3]
				colour = true_colours[pn][2] - true_colours[pn][3] #V-I	
			
	
			pn_mags = tab[pn]
	 		for block in pn_mags:
 	 			if block[0][0] == night:
					for line in block:
						if line[1]== filtername:
							#cols = ['Night', 'Filter', 'Airmass', 'mag', 'mag_err']
							filter_data.append([line[2], line[3], line[4], colour, true])


		"""	
		for line in filter_data:
			print line
			raw_input('')
		diff = [ float(line[1])-float(line[3]) for line in filter_data]
		z = [line[0] for line in filter_data]
		plt.plot(z, diff, 'o')
		plt.show()
		"""
	
		true = np.array([line[4] for line in filter_data])
		#temp = airmass, inst_mag, err, colour
		temp = [ [line[0], line[1], line[2], line[3] ] for line in filter_data ]
		
		print night 
		print len(temp), 'objects'
		for line in temp:
			print line
		print
		
		if len(temp)==0 : continue
		


		#x = airmass, mag, err, colour
		def mag_transform(x, O, C, K):
			return O + x[1] + (C*x[3]) - (K*x[0])


		popt, pcov = curve_fit(mag_transform, np.transpose(temp), true)
		print
		print popt
		print pcov

		#Y = true_mag - O - inst_mag - C*colour
		Y = [line[4] - popt[0] - line[1] - popt[1]*line[3] for line in filter_data]		
		airmass = [line[0] for line in filter_data]
		
				
		zipped = zip(airmass, Y, true)
		for line in zipped:
			print line
		
		x = np.linspace(min(airmass), max(airmass), 100)
		y = [-popt[2]*val for val in x]
 	
		plt.figure()
		plt.plot( airmass, Y, 'o')
		plt.plot(x, y, 'k--')
		plt.ylabel('Y1')
		plt.xlabel('Airmass')
		plt.title(night+','+filtername)
		plt.show()

 
 
 
 
 
 
 
 
 
 
 
 
 


