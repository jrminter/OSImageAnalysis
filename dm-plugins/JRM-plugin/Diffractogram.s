// Diffractogram_v1.s  version1.0b0 1997-10-20
//
//
// This script may be distributed freely if   unchanged !
// suggest: (check final length of image name interactive)
//
// Useful:  peak_v1.s to evaluate diffracted beam position/intensity
//

   image front, hannX, hannY, hanning, diffractogram
   image temp, rotational_average, dst, line_projection
   number top, left, bottom, right, posX, posY, sizeX, sizeY, sizeXx, sizeYy
   number test, nns, scaleX, scaleY, calibrate, stringlength
   number scaleXx, scaleYy, scaleXF, scaleYF, const1, ii, zoom
   string pixelSizeUnit, pixelSizeUnitF, testunit, selection, History, oriName, strOutFile
   number samples = 360, xscale, yscale, xsize, ysize
   number centerx, centery, k, halfMinor
   number i, dInt, bRet, iCrop



   try
      front := GetfrontImage()
   catch
      Throw("Diffractogram_v1.s\n\nOnly for real or integer images ...\n(or, no image found)")

   oriName = GetName(front)
   GetSize( front, sizeX, sizeY)
   GetSelection( front, top, left, bottom, right )
   GetScale( front, scaleX, scaleY)
   GetWindowPosition( front, posX, posY)
   zoom = GetZoom(front)
   sizeXx = right - left 	
   sizeYy = bottom - top	
   scaleXx = scaleX * (sizeXx / sizeX)
   scaleYy = scaleY * (sizeYy / sizeY)
   scaleXF = 1/( scaleXx * sizeX )
   scaleYF = 1/( scaleYy * sizeY )
   pixelSizeUnit = GetUnitString( front )
   if(pixelSizeUnit != "")
   {
      calibrate = 1
      testUnit = left( pixelSizeUnit, 1)
      stringlength = len(pixelSizeUnit)
      if( testUnit != "1")
         pixelSizeUnitF = "1/" + pixelSizeUnit
      else
         pixelSizeUnitF = right( pixelSizeUnit, stringlength - 2)
   }
   if(sizeX/sizeXx > 1)
      selection = "yes"
//
// create Hanning window:
//
   OpenAndSetProgressWindow( "Calculating", "Hanning window", " ..." )
   const1 = 2 * Pi() / sizeXx
   hannX := CreateFloatImage("", sizeXx, sizeYy)
   hannX = 0
   hannX[0,0,1,sizeXx] = 1 - cos( const1 * icol )
   ii = 1
   while( ii < sizeXx )
   {	
      hannX[ii, 0, 2*ii, sizeXx] = hannX[0, 0, ii, sizeXx]
      ii = ii * 2
   }	
   hannY = hannX + 0;
   RotateLeft(hannY)
   hanning = hannX * hannY

//
// Apply Hanning window to image, do FFT, take modulus
//
   OpenAndSetProgressWindow( "Calculating", "diffractogram", " ..." )
   diffractogram := front[ top, left, bottom, right ] * hanning
   diffractogram = modulus( RealFFT( diffractogram ) )

//
// add history tree:
//
   History = GetStringNote(front, "History:[0]")	//	version 3.1 ..
   if(History == "")
      AddStringToList( diffractogram, "History", "" + GetName(front))
   else
   {	
      ii = 0
      History = "??"
      while(History != "")
      {	
         try
            History = GetStringNote(front, "History:[" + ii + "]")
         catch
         {	
            History = ""
            break
         }	
         if(History != "")
            AddStringToList(diffractogram, "History", History)
         ii += 1
      }	
   }	

//		
//		add new history
//		
   if( selection == "yes")	
   {
      AddStringToList(diffractogram, "History", "selection: ["+top+","+left+","+bottom+","+right+"]")
      AddStringToList(diffractogram, "History", "* Hanning window")
      AddStringToList(diffractogram, "History", "FFT")
      AddStringToList(diffractogram, "History", "Modulus")
      SetName( diffractogram, GetName( front ) + ".s.Dif" )
   }
   else
   {
      AddStringToList(diffractogram, "History", "* Hanning window")
      AddStringToList(diffractogram, "History", "FFT")
      AddStringToList(diffractogram, "History", "Modulus")
      SetName( diffractogram, GetName( front ) + ".Dif" )
   }
//
// handle display and scaling
//
SetZoom( diffractogram, zoom )
SetScale( diffractogram, scaleXF, scaleYF)
SetName(diffractogram, oriName+"-ps")
SetUnitString( diffractogram, pixelsizeunitF)
DisplayAt( diffractogram, posX + 10, posY + 17 )
SetSurvey( diffractogram, 1)
UpdateImage( diffractogram )

CloseProgressWindow()

GetSize( diffractogram, xsize, ysize )
halfMinor = min( xsize, ysize )/2

centerx = xsize / 2
centery = ysize / 2

dst := CreateFloatImage( "dst", halfMinor, samples )
k = 2 * pi() / samples


dst = warp( diffractogram, icol*sin(irow*k) + centerx, icol*cos(irow*k) + centery )
line_projection := CreateFloatImage( "line projection", halfMinor, 1 )
line_projection = 0
line_projection[icol,0] += dst
line_projection /= samples

bRet = GetPersistentNumberNote("Diffractogram:CropCenter", iCrop);
if (bRet < 1)
{
   iCrop = 5;
   SetPersistentNumberNote("Diffractogram:CropCenter", iCrop);
}

// crop center
for(i=0; i<iCrop; i++)
{
  line_projection[i,0] = 0
}

strOutFile = oriName + "-ps-ra.csv"
if(SaveAsDialog( "Save Profile", strOutFile, strOutFile ))
{
   number nFile = CreateFileForWriting(strOutFile )
   WriteFile( nFile, 0, " R [px], I\n" );
   for( i = 0; i < halfMinor; ++i )
   {
      dInt = GetPixel(line_projection,i,0);
      WriteFile( nFile, 0, i + "," + dInt + "\n" );
   }
      CloseFile( nFile )
}

SetName(line_projection , oriName + "-ps-ra")


// clean up
DeleteImage(dst)
ShowImage( line_projection )
