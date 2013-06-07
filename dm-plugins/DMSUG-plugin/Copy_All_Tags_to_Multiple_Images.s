// Script to copy ALL the tags from a user selected image to all other displayed images.
// This script would be used for copying tags from an image
// acquired in th usual manner, to images synthesised by
// processing - for example jump ratio images.
// The script also adds a scale bar to the images if one is not present.


// D. R. G. Mitchell, rm@ansto.gov.au
// version 1.0, Dec 2004

// Variables

image imgsource, imgtarget

// counts the number of open images - any hidden images are ignored
Number kWINDOWTYPE_IMAGEWINDOW = 5
number numberDocs = CountDocumentWindowsOfType(kWINDOWTYPE_IMAGEWINDOW) 

if(numberdocs<2)
	{
		beep()
		okdialog("Two or more images must be displayed to use this script!")
		exit(0)
	}

string targetname, sourcename
number i
number inc=30 // this is the increment that steps the images across the screen

beep()
if(!twobuttondialog("This script will transfer all tags - Microscope Info, etc.from the\nimage you select to all open images. Hidden images are ignored.\n\nExisting tag info is overwritten without warning!", "Proceed","Abort")) exit(0) 
// puts up a dialog to select an image, extis if cancel is pressed
try
	getoneimagewithprompt("Select Image to Source Tags From: ","Multiple Tag Transfer", imgsource)

catch
	exit(0)

// Sets the selected image foremost and gets the tag information from it
showimage(imgsource)
setwindowposition(imgsource, 142,24)
updateimage(imgsource)
sourcename=getname(imgsource)
TagGroup sourcetags=imagegettaggroup(imgsource)


// Loops through the open images transferring the tags, adding a scale bar and cascading them across the screen
for( i = 1; i < numberDocs; ++ i )
	{
		// work through the images selecting them in turn
		ImageDocument imgDoc = GetImageDocument(i)
		imgtarget:=imagedocumentgetimage(imgdoc,0)
		targetname=getname(imgtarget)

		// transfer the tags from the source image to the target image
		TagGroup targettags=imagegettaggroup(imgtarget)
		taggroupcopytagsfrom(targettags,sourcetags)

		// check for a scale bar. If one is not present add one.
		ImageDisplay display = imgtarget.ImageGetImageDisplay(0)
		Number hasScaleBar = display.ComponentCountChildrenOfType(31) // 31 is the type number of a scale bar
		if (!hasScaleBar)
		display.ApplyDataBar()

		// Cascade across the screen
		imagedocumentshowatposition(imgdoc,142+inc, 24+inc)
		inc=inc+30
	}

okdialog("All tags copied from '"+sourcename+"' to "+(i-1)+" images")