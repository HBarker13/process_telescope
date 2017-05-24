#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Use the calibration factors made by mags_tab_sq_fits.py to calculate the true CS magntidues from the instrumental ones.
CS mags are the average ones, calculated using calc_avg_mags.py, which takes the results from daophot_wrapper.py as input.
Coefficient values (calculated by mag_sq_fit.py) are those from daophot_wrapper.py, NOT the averaged magnitudes"""


import numpy as np
from matplotlib import pyplot as plt 
from scipy.optimize import curve_fit
import os
import sys
import math


#read in instrumental mags, and calibration values
working_dir = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU'
calib_path = working_dir + '/calib_coeffs.tab'
cs_mags_path = working_dir + '/avg_cs_mags.tab'


#read in calibration values
#Night	Filter	O	O_err	K	K_err	C	C_err	
with open(calib_path, 'r') as f:
	calib_tab = [line.strip().split() for line in f]	

#read in instrumental magnitudes
#Star	Night	Filter	Airmass	Mag	Mag_err	
with open(cs_mags_path, 'r') as f:
	raw_mags = [line.strip().split() for line in f]
	
	
#skip the first lines, which are column names
calib_tab = calib_tab[1:]
raw_mags = raw_mags[1:]	
			
#get object names
names = set( [line[0] for line in raw_mags] )	

nights = ['Night1', 'Night2', 'Night3']	
filtername = ['U', 'B', 'V', 'I']
	

	
#loop through objects
for name in names:
	if name!='K1-22': continue
	print name
	
	for night in nights:
		if night!='Night2':continue
		print night
		
		#average instrumental mags
		inst_mags = [ line for line in raw_mags if line[0]==name and line[1]==night]

		U=None
		B=None
		V=None
		I=None
		
		for line in inst_mags:
			if line[2]=='U': U = line
			elif line[2]=='B': B = line
			elif line[2]=='V': V = line
			elif line[2]=='I': I = line
			else:
				print 'Error: filtername problem'
				print line
				sys.exit()
						
				
		O_U = None
		K_U = None
		C_U = None
		
		O_B = None
		O_B = None
		O_B = None
		
		O_V = None
		O_V = None
		O_V = None
		
		O_I = None
		O_I = None
		O_I = None		

		#find the correct calibration values
		for l in calib_tab:
			if l[0]==night:
				if l[1]=='U':
					O_U = float( l[2] )
					K_U = float( l[4] )
					C_U = float( l[6] )
					
					O_U_err = float( l[3] )
					K_U_err = float( l[5] )
					C_U_err = float( l[7] )
					
				elif l[1]=='B':
					O_B = float( l[2] )
					K_B = float( l[4] )
					C_B = float( l[6] )	
					
					O_B_err = float( l[3] )
					K_B_err = float( l[5] )
					C_B_err = float( l[7] )
		
				elif l[1]=='V':
					O_V = float( l[2] )
					K_V = float( l[4] )
					C_V = float( l[6] )
										
					O_V_err = float( l[3] )
					K_V_err = float( l[5] )
					C_V_err = float( l[7] )
					
				elif l[1]=='I':
					O_I = float( l[2] )
					K_I = float( l[4] )
					C_I = float( l[6] )
					
					O_I_err = float( l[3] )
					K_I_err = float( l[5] )
					C_I_err = float( l[7] )

		
		try:
			u = float(U[4])
			u_err = float(U[5])
			U_airmass = float( U[3] )
		except:
			u = None
			U_airmass = None
		
		try:
			b = float(B[4])
			b_err = float(B[5])
			B_airmass = float( B[3] )
		except:
			b = None
			B_airmass = None
		
		try:	
			v = float(V[4])
			v_err = float(V[4])
			V_airmass = float( V[3] )
		except:
			v = None
			V_airmass = None
			
		try:	
			i = float(I[4])
			i_err = float(I[4])
			I_airmass = float( I[3] )
		except:
			i = None
			I_airmass = None
			
				
				
		#first run		
		U = u
		B = b
		V = v
		I = i		
			
		#loop until the values converge	
		test = 100.	
		counter = 0
		while(test>0.000000001):	
		
			U_prev = U
			B_prev = B
			V_prev = V
			I_prev = I
				
			U = ( 1 / (1-C_U) ) * ( O_U + u - (K_U*U_airmass) - (C_U*B ) )
			B = ( 1 / (1-C_B) ) * ( O_B + b - (K_B*B_airmass) - (C_B*V ) )
			V = ( 1 / (1+C_V) ) * ( O_V + v - (K_V*V_airmass) + (C_V*B ) ) #not a typo
			I = ( 1 / (1+C_I) ) * ( O_I + i - (K_I*I_airmass) + (C_I*V ) )
			
			
			#calculate error
		
			#Orsola calulated errors:
			#Berr**2 = O_err**2 +  b_err**2 + ( (B-V)**2 * C_err**2 ) + ( C_err**2 * B-V_err**2 ) + ( airmass_err**2 * Kerr**2 ) + apcor_err**2
		
			#where B-V_err is some complicated thing  
			
			
			
		
		
			test = math.sqrt( ( (U-U_prev)**2 + (B-B_prev)**2 + (V-V_prev)**2 + (I-I_prev)**2 ) )
		
			counter+=1
			if counter>1000:
				print 'Counter >1000'
				print 'Convergence failed:', night, name
				raw_input('')
		

		print 'DONE'



		
		
			

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		


 
 
 
 
 


