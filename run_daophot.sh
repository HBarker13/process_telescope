#!/bin/bash
#Run daophot photometry
#needs to be run from the directory


# Get rid of any junk files which DAOPHOT has left lying around.
rm -f *jnk.sdf	

#read in files
fitsfiles=$PWD/*.fits


echo "Enter frame number: "
read in_num
echo

#convert each fits file to a ndf file
for f in $fitsfiles
do

	#filenames are often too long and need shortening
	#for daophot?

	filename=$(basename "$f")
	fileparts="${filename#*.}"
	framenum="${fileparts#*-}"
	framenum="${framenum%%_*}"
	

	if [ "$in_num" != "$framenum" ]; then
	continue
	fi
	
	#copy the file to a new shorter name
	newname=$framenum".fits"
	cp $f $newname

	echo $f
	"/star/bin/convert/fits2ndf" "$newname" "${newname/.fits/.sdf}"
	echo

	#delete the copied original file
	rm $newname


	filename="${newname/.fits/.sdf}"
	echo "Created " $filename



#  Get filename without the .sdf extension.
	extension="${filename##*.}"
	fileroot="${filename%.*}"


	# Get rid of any junk files which DAOPHOT has left lying around.
	rm -f *jnk.sdf	 
	rm -f "$fileroot.ap"
	rm -f "$fileroot.coo"
	rm -f "$fileroot.lst"
	rm -f "$fileroot.psf"
	    
         
#Prompt user for FWHM
	echo -n "Enter the FWHM in pixels and press [ENTER]:"
	read fwhm
	
	#bash can't handle non-integer math, need to use bc
	fwhm2=$(echo $fwhm*2.0 | bc)
	fwhm4=$(echo $fwhm*4.0 | bc)
	fwhm5=$(echo $fwhm*5.0 | bc)
	
	
#create fwhm commands to feed into daophot
	fwhm_cmd='FWHM='$fwhm
	fit_cmd='FIT='$fwhm2
	psf_cmd='PSF='$fwhm4
	
	inner_rad='IS='$fwhm4
	outer_rad='OS='$fwhm5




#need to write these to the files
	daophot_opt=$PWD/daophot.opt
	rm -f $daophot_opt
	echo $fwhm_cmd >> $daophot_opt
	echo $fit_cmd >> $daophot_opt
	echo $psf_cmd >> $daophot_opt
	echo "READ=4.57" >> $daophot_opt
	echo "GAIN=1.04" >> $daophot_opt
	echo "TH=3.0" >> $daophot_opt
	echo "AN=1" >> $daophot_opt
	echo "LOWBAD=5" >> $daophot_opt
	echo "HIBAD=50000" >> $daophot_opt
	echo "WATCH=1" >> $daophot_opt
	echo "VAR=0" >> $daophot_opt
	
	echo "Written " $daophot_opt
	echo
	
	photo_opt=$PWD/photo.opt
	rm -f $photo_opt
	echo "A1=3.0" >> $photo_opt
	echo "A2=4.0" >> $photo_opt
	echo "A3=5.0" >> $photo_opt
	echo "A4=6.0" >> $photo_opt
	echo "A5=7" >> $photo_opt
	echo "A6=8" >> $photo_opt
	echo "A7=9" >> $photo_opt
	echo "A8=10" >> $photo_opt
	echo "A9=" >> $photo_opt
	echo "AA=" >> $photo_opt
	echo "AB=" >> $photo_opt
	echo "AC=" >> $photo_opt
	echo $inner_rad >> $photo_opt
	echo $outer_rad >> $photo_opt
	
	echo "Written " $photo_opt
	echo
	
	
	allstar_opt=$PWD/allstar.opt
	rm -f $allstar_opt
	echo $fit_cmd >> $allstar_opt
	echo $inner_rad >> $allstar_opt
	echo $outer_rad >> $allstar_opt
	echo "WATCH=1.0" >> $allstar_opt
	echo "redet=1" >> $allstar_opt
	
	echo "Written " $allstar_opt
	echo
     

#  Write filename to screen.
         echo "***"
         echo "*** Processing file $filename ***"
         echo "***"
         

         
#	start daophot
	source /star/bin/daophot/daophot.csh


#  Run DAOPHOT with the appropriate commands. LEAVE UNINDENTED
# For pick, I want 30 objects no fainter than 25 mags
	/star/bin/daophot/daophot <<__DAOPHOT-END__
ATTACH $fileroot
FIND
1,1
$fileroot
Y
PHOT
YES
A1=3.0
A2=4.0
A3=5.0
A4=6.0
A5=7.0
A6=8.0
A7=9.0
A8=10.0
$inner_rad
$outer_rad
YES
$fileroot.coo
$fileroot.ap
PICK
$fileroot.ap
30,25
$fileroot.lst
EXIT
__DAOPHOT-END__
#PSF
#$fileroot.ap
#$fileroot.lst
#30



#  Get rid of scratch file that DAOPHOT has written.
#         rm ${fileroot}jnk.sd


done
































