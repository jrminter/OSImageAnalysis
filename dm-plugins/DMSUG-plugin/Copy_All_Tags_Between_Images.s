// Script to copy ALL the tags from one image to another.
// This script would be used for copying tags from an image
// acquired in th usual manner, to one which was synthesised by
// processing - for example a diffraction pattern bolted together from two halves.
// Such processed images do no have any microscope info attached to them, and this is used for Cumulus
// archival - so it is important


// D. Mitchell Nov 2002
// drm@ansto.gov.au
// Version 1.0


image imgsource, imgtarget

try
gettwoimageswithprompt("0 = Source Image, 1 = Target Image","Copy ALL tags between images", imgsource, imgtarget)

catch
exit(0)

string targetname, sourcename
targetname=getname(imgtarget)
sourcename=getname(imgsource)

TagGroup sourcetags=imagegettaggroup(imgsource)
TagGroup targettags=imagegettaggroup(imgtarget)
taggroupcopytagsfrom(targettags,sourcetags)

showimage(imgsource)
showimage(imgtarget)
okdialog("All tags copied from '"+sourcename+"' to '"+targetname+"'.")