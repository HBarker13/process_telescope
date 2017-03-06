# process_telescope


1. overscan_correct.py.
Reads in files with format T2M3Im-yymmdd.time-00##.fits (bias, flat and science frames).
Looks at the overscan region (the leftmost two columns), calculates the mean pixel value, and subtracts this from all pixels. 
Makes newfiles with the format T2M3Im-yymmdd.time-00##_ovscorr.fits


2. master_bias.py
Reads in overscan corrected bais frames from each night and calculates the median value for each pixel, and saves this as a master bias.  (The mean can also be calculated)


3. debias.py
Reads in the master bias for each night, and debiases the overscan corrected science and flat files.
Creates files with the format T2M3Im-yymmdd.time-00##_ovscorr_debiased.fits

NB. debias.py removes the T2M3Im-yymmdd.time-00##_ovscorr.fits file. This can be commented out


4. master_flat.py
Creates a master flat in each filter from the median of the overscan corrected, debiased flat files. NOTE: flat frames in each filter were not taken every night.


5. deflat.py
Flat-field corrects frames of with the matching filter (from any night).




Misc: clear_all.py
Deletes all processed files (ie. overscan corected, debiased, flat corrected and master flat and bias frames) so the Sorted directory contains only the raw data.
