// Script to close all images
Number kWINDOWTYPE_IMAGEWINDOW = 5
number numberDocs = CountDocumentWindowsOfType(kWINDOWTYPE_IMAGEWINDOW)
number i

for( i = 0; i < numberDocs; ++ i )
{
   ImageDocument imgDoc = GetImageDocument( 0 )
   image img:=getfrontimage()
   imagedocumentClose(imgdoc,0)
}

numberDocs = CountDocumentWindowsOfType(kWINDOWTYPE_IMAGEWINDOW)

// Loop to close all the hidden images
while(3>2)
{
	try
	{
		imagedocument img=getimagedocument(numberDocs)
		imagedocumentclose(img,0)
	}
	Catch
	{
		exit(0)
	}
}
