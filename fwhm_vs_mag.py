#!/mirror/scratch/hbarker/pkgs/anaconda/bin/python

"""Plot wrapper mags as a function of airmass / fwhm"""

from matplotlib import pyplot as plt



#wrapper_fpath = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/wrapper_standard_mags.tab'

wrapper_fpath = '/mirror2/scratch/hbarker/Orsola_2.3m_ANU/daophot_params_test/standard_mags.tab'


with open(wrapper_fpath, 'r') as f:
	tab = [line.strip().split() for line in f]
	
colnames = tab[0]
tab = tab[1:]

#tab = [line for line in tab if line[4]=='20']


mag = [ line[-2] for line in tab]
airmass = [ line[5] for line in tab]


plt.figure()
plt.plot(airmass, mag, 'o')
plt.xlabel('Airmass')
plt.ylabel('Mag')
plt.show() 	
