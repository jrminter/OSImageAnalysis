// Script to cut out the ROI in the foremost image and
// create a new image from it.

// D. R. G. Mitchell, drm@ansto.gov.au
// Version 1.1
// Modified by JRM 24-Mar-2006
// Make a longer image name

// variables

number sizex, sizey, scalex, scaley
number top, left, bottom, right
number roipixwidth, roiunitwidth, roipixheight, roiunitheight
string unitstring, imgname


// Get info from foremost image

image front:=getfrontimage()
getsize(front, sizex, sizey)
getscale(front, scalex, scaley)
getunitstring(front, unitstring)
getname(front, imgname)


// Check for presence of ROI - error if absent

imagedisplay imgdisp=front.imagegetimagedisplay(0)
number roinumber=imgdisp.imagedisplaycountrois()

if(roinumber!=1) 
	{
		beep()
		okdialog("A rectangular Region Of Interest (ROI) must be present for this script to work!")
		exit(0)
	}


// Get ROI parameters

roi theroi=imgdisp.imagedisplaygetroi(0)
roigetrectangle(theroi, top, left, bottom, right)

roipixwidth=right-left
roiunitwidth=roipixwidth*scalex
roipixheight=bottom-top
roiunitheight=roipixheight*scaley


// Give info on the ROI being used

okdialog("Region selected for extraction is : \n"+roipixwidth+" pixels wide ("+roiunitwidth+" "+unitstring+")\n"+roipixheight+" pixels high ("+roiunitheight+" "+unitstring+")\nTop left corner is at x = "+left+" y = "+top)


// Copy the selected region and create a new image

scrapcopy(front)
scrappastenew()


// Calibrate and name the new image

image cropped:=getfrontimage()
setscale(cropped, scalex, scaley)
imagedisplay cropdisp=cropped.imagegetimagedisplay(0)
cropdisp.applydatabar()
number substringlength=len(imgname)
if(substringlength>9) substringlength=9
string shortname=left(imgname, substringlength)+" Extracted ROI"
string longname = imgname + " ROI"
setname(cropped, longname )