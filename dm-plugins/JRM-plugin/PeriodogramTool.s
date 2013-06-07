// Script to compute a periodogram from an image
// uses Welch method. Provides an rotational average
// of the sq. modulus, outputting the data to a
// .csv file. It writes the spatial frequency in the
// 1/A
//
// Tested underunder GMS 1.8 and 2.1
//
// The module displays the the line profile as a
// semi-log line profile. One can also
// choose to crop the center of the FFT or to limit to the
// half Nyquist limit for better display.
//
// Uses ideas from HanningFFT.s by Ruben Bjorge of NTNU
// and especially P. D. Welch et al., "The Use of Fast Fourier
// Transform for the Estimation of Power Spectra: A Method Based
// on Time Averaging Over Short, Modified Periodograms", IEEE
// Transactions on Audio Electroacoustics, Volume AU-15 (June 1967),
// pages 70-73. cf http://en.wikipedia.org/wiki/Welch's_method
// Also uses ideas from the Gatan Scripting section of the DM User Manual
//
//
// Created JRM 2006-12-13
//
// Modifcation History:
//
//   Date        Who   What...
// -----------   ---   ----------------------------------------------------------
// 2007-10-25    JRM   Added overlap computation and Hanning Window
// 2007-10-26    JRM   Fixed limits on loop. Call this version 1.1
// 2007-11-22    JRM   Moved stored tags to Periodogram group
//                     Call this version 1.2
// 2007-11-23    JRM   Crop out center half. Call this version 1.3
// 2008-12-20    JRM   Made limit to half Nyquist an option - v 1.4
// 2008-12-22    JRM   Major edit. Added a dialog interface to better manage
//                     persistent data and to make a more polished interface.
//                     Renamed PeriodogramTool and changed version to 2.0
// 2010-03-03    JRM   Added ability to use sqrt(mod). Changed version to 2.1
// 2010-06-30    JRM   Added ability to transform display gamma.
//                     Changed version to 2.2
// 2013-05-29    JRM   Removed underscores from names
//                     Versions 2.2.1
//
// This script is released under the Gnu Public License v.2
// http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

image CreateHanningWindow(number nWidth, number nHeight)
{
   // Create Hanning window.
   number i
   image imgHannX, imgHannY, imgHann

   i = 1
   imgHannX := CreateFloatImage("", nWidth, nHeight)
   imgHannX = 0
   imgHannX[0, 0, 1, nWidth] = 1 - cos( 2 * Pi() * icol / nWidth)
   while( i < nHeight )
   {
       imgHannX[i, 0, 2*i, nWidth] = imgHannX[0, 0, i, nWidth]
       i = i * 2
   }

   i = 1
   imgHannY := CreateFloatImage("", nWidth, nHeight)
   imgHannY = 0
   imgHannY[0, 0, nHeight, 1] = 1 - cos( 2 * Pi() * irow / nHeight)
   while( i < nWidth )
   {
       imgHannY[0, i, nHeight, 2*i] = imgHannY[0, 0, nHeight, i]
       i = i * 2
   }

   imgHann = imgHannX * imgHannY
   CloseImage(imgHannX)
   CloseImage(imgHannY)
   return imgHann
}

TagGroup PDT_Dlg, PDT_DlgItems

Taggroup PDT_Label1 = DLGCreateLabel( "Compute periodogram from front image")
Taggroup PDT_Label2 = DLGCreateLabel( "V2.2.1  (c) J. R. Minter under GPL 2.0")
Taggroup PDT_Label3 = DLGCreateLabel( "Start Gamma at 0.5, then adjust     ")

Taggroup PDT_CropInnerRadius, PDT_CropInnerRadiusField
Taggroup PDT_FFTsize, PDT_FFTsizeField
Taggroup PDT_Overlap, PDT_OverlapField
Taggroup PDT_Gamma, PDT_GammaField
Taggroup PDT_MaxLimitFr, PDT_MaxLimitFrField

Taggroup PDT_CropCenterBox
Taggroup PDT_UseSqrtBox
Taggroup PDT_LimitHalfNyquistBox
Taggroup PDT_SaveCsvBox
Taggroup PDT_ShowLinePlotBox

Taggroup PDT_ComputePeriodogramButton
Object   objPDToolWindow

// global variables for persistent values
number g_nCropInnerRadius, g_nFFTsize, g_nOverlap, g_nGamma, g_nMaxLimitFr
number g_bCropCenter, g_bLimitHalfNyquist
number g_bSaveCsvFile, g_bShowLinePlot
number g_bUseSqrt


// This bit of code is where buttons and pulldowns generate responses.
class PDTool : uiframe
{
   void compute_periodogram(object self)
   {
      // get values from DLG and save
      g_nCropInnerRadius = PDT_CropInnerRadius.DLGGetValue()
      SetPersistentNumberNote("Periodogram:CropInnerRadius", g_nCropInnerRadius)

      g_nFFTsize = PDT_FFTsize.DLGGetValue()
      SetPersistentNumberNote("Periodogram:SizeFFT", g_nFFTsize)

      g_nOverlap = PDT_Overlap.DLGGetValue()
      SetPersistentNumberNote("Periodogram:Overlap", g_nOverlap)

        g_nGamma = PDT_Gamma.DLGGetValue()
      SetPersistentNumberNote("Periodogram:Gamma", g_nGamma)

        g_nMaxLimitFr = PDT_MaxLimitFr.DLGGetValue()
      SetPersistentNumberNote("Periodogram:MaxLimitFr", g_nMaxLimitFr)


      g_bCropCenter = PDT_CropCenterBox.DLGGetValue()
      SetPersistentNumberNote("Periodogram:CropCenter", g_bCropCenter)

      g_bUseSqrt = PDT_UseSqrtBox.DLGGetValue()
      SetPersistentNumberNote("Periodogram:UseSqrt", g_bUseSqrt)

      g_bLimitHalfNyquist = PDT_LimitHalfNyquistBox.DLGGetValue()
      SetPersistentNumberNote("Periodogram:LimitHalfNyquist", g_bLimitHalfNyquist)

      g_bSaveCsvFile = PDT_SaveCsvBox.DLGGetValue()
      SetPersistentNumberNote("Periodogram:SaveCsvFile", g_bSaveCsvFile)

      g_bShowLinePlot = PDT_ShowLinePlotBox.DLGGetValue()
      SetPersistentNumberNote("Periodogram:ShowLinePlot", g_bShowLinePlot)

      // local variables
      image front
      number i, j, k
      image cropped, dst, line_projection, ITT
      compleximage theFFT
      realimage theReal, theImag, theMod, cropMod, logMod
      ImageDisplay theDisp

      number sizex, sizey, scalex, scaley, halfMinor
      number top, left, bottom, right
      number roipixwidth, roiunitwidth, roipixheight, roiunitheight
      string unitstring, imgname, strFftUnit
      number dMin, dMax, dMean, dStdDev
      number nMax=256


      number centerx, centery
      number dScaleFactor = 1
      number dIntFactor
      number samples = 256
      number dAngPerPix, dDeltaS
      number dAvgGray = 0.0
      number dFractCutOff = 0.95
      number dTempFactor = 0.05

      // prepare intensity transform for gamma
      dIntFactor = g_nFFTsize*g_nFFTsize

      ITT:=RealImage("",4,nMax,1)
      ITT=icol/nMax
      ITT=nMax*exp((1-g_nGamma)/g_nGamma*log(ITT))
      ITT=min(ITT,nMax)

      // Make sure we have a place to write results...

      OpenResultsWindow()

      // Get info from foremost image

      front:=getfrontimage()
      dMean = mean(front)
      dStdDev = sqrt(variance(front))
      getsize(front, sizex, sizey)

      getscale(front, scalex, scaley)
      getunitstring(front, unitstring)
      if(unitstring == "nm")
      {
         dScaleFactor = 10.0
      }
      if(unitstring == "µm")
      {
         dScaleFactor = 10000.0
      }

      dAngPerPix = dScaleFactor * scalex
      dDeltaS = 1.0 / (dAngPerPix * g_nFFTsize)


      getname(front, imgname)

      TagGroup	tgImgParams = front.ImageGetTagGroup()
      number nVoltage
      tgImgParams.TagGroupGetTagAsNumber( "Microscope Info:Voltage", nVoltage )
      number nCs
      tgImgParams.TagGroupGetTagAsNumber( "Microscope Info:Cs(mm)", nCs )




      Result("Image: " + imgname + ", scale = " + dAngPerPix + " Å/px\n")
      Result("FFT scale:  = " + dDeltaS + " [[1/Å]/px]\n")
      strFftUnit = "1/"+unitstring
      k=0

      Image imgHanning

      top      = 0
      bottom   = g_nFFTsize
      left     = 0
      right    = g_nFFTsize

      imgHanning = CreateHanningWindow(g_nFFTsize, g_nFFTsize)

      k = 0
      bottom = g_nOverlap
      right = g_nOverlap

      // Result ("Width =  " + sizex + ", Height =  " + sizey + "\n")

      // process the pieces
      while (bottom < (sizey - g_nOverlap))
      {
         top = bottom - g_nOverlap
         bottom = top + g_nFFTsize
         // be sure we are in bounds along y...
         if( bottom <= sizey)
         {
            // Result ("Top =  " + top + ", Bottom =  " + bottom + "\n")
            while (right < (sizex - g_nOverlap))
            {
               left = right - g_nOverlap
               right = left + g_nFFTsize

               // be sure we are in bounds along x...
               if( right <= sizex)
               {
                  // Result ("Left =  " + left + ", Right =  " + right + "\n")
                  cropped=front[top,left, bottom, right ]
                  cropped = (cropped - dMean)/dStdDev
                  cropped = cropped * imgHanning
                  setscale(cropped, scalex, scaley)
                  theFFT := RealFFT(cropped)
                  theReal := real(theFFT)
                  theImag := imaginary(theFFT)
                  if(k < 1)
                  {
                    theMod = theReal*theReal + theImag*theImag
                  }
                  else
                  {
                    theMod += theReal*theReal + theImag*theImag
                  }
                  k=k+1
               } // end if right
             } // end while right
             right = g_nOverlap

           } // end if bottom

         } // end while bottom

         Result ("Averaged " + k + " pieces of size " + g_nFFTsize +"x"+ g_nFFTsize + "\n")
         number sMax = 1/(2*scalex)
         number deltaS = sMax/(g_nFFTsize/2)
         setscale(theMod, deltaS, deltaS)
         setunitstring(theMod, strFftUnit)
         theMod /= k
         dMax = max(theMod)
         if (g_bCropCenter > 0)
         {
           theMod=tert(iradius> g_nCropInnerRadius, theMod, dMax/1000000)
         }
         deleteimage(theFFT)
         deleteimage(theReal)
         deleteimage(theImag)
         deleteimage(cropped)
         deleteimage(imgHanning)

         if (g_bUseSqrt > 0)
         {
            theMod = max(theMod, 0)
            theMod = sqrt(theMod)
         }




         setsurveytechnique(theMod, 1)
         setsurvey(theMod,1)
         SetName(theMod, "PS-"+imgname)
         showImage(theMod)
         dMin = min(theMod)
         dMax = max(theMod)
         result("Dmin = " + dMin + "Dmax = " + dMax)
         SetLimits(theMod, dMin, dMax)
         updateimage(theMod)









         string strOutFile, strRotAvg
         number nFile
         number dS, dI

         if (g_bLimitHalfNyquist > 0)
         {
            // create a rectangle ROI
            ROI theroi = NewROI( )
            top = g_nFFTsize / 4
            left = top
            bottom = 3*g_nFFTsize/4
            right = bottom
            imagedisplay mod_disp=theMod.imagegetimagedisplay(0)
            number roinumber= mod_disp.imagedisplaycountrois()
            theroi.ROISetRectangle( top, left, bottom, right )
            mod_disp.ImageDisplayAddROI(theroi)
            cropMod = theMod[]
            setscale(cropMod, deltaS, deltaS)
            setunitstring(cropMod, strFftUnit)
            deleteimage(theMod)
            SetName(cropMod, imgname + "-ps")

            tgImgParams = cropMod.ImageGetTagGroup()
            tgImgParams.TagGroupSetTagAsNumber( "Microscope Info:Voltage", nVoltage )
            tgImgParams.TagGroupSetTagAsNumber( "Microscope Info:Cs(mm)", nCs )

            showImage(cropMod)

            theDisp=cropMod.ImageGetImageDisplay(0)
            theDisp.ImageDisplaySetIntensityTransformation(ITT)
            dMin = min(cropMod)
            dMax = max(cropMod)
            result("Dmin = " + dMin + "Dmax = " + dMax)
            SetLimits(cropMod, dMin, g_nMaxLimitFr*dMax)
            // updateimage(cropMod)
            showimage(cropMod)




            getsize(cropMod, sizex, sizey)
            halfMinor = min( sizex, sizey )/2
            centerx = sizex / 2
            centery = sizey / 2


            strOutFile = imgname +"-ra-ps.csv"
            strRotAvg = imgname + "-ra-ps"


            dst := CreateFloatImage( "dst", halfMinor, samples )
            k = 2 * pi() / samples
            dst = warp( cropMod, icol*sin(irow*k) + centerx, icol*cos(irow*k) + centery )
         }
         else
         {
            // theMod=min(theMod,nMax)
            theDisp=theMod.ImageGetImageDisplay(0)	
            theDisp.ImageDisplaySetIntensityTransformation(ITT)
            dMin = min(theMod)
            dMax = max(theMod)
            result("Dmin = " + dMin + "Dmax = " + dMax)
            SetLimits(theMod, dMin, g_nMaxLimitFr*dMax)
            //updateimage(theMod)
            showimage(theMod)

            getsize(theMod, sizex, sizey)
            halfMinor = min( sizex, sizey )/2
            centerx = sizex / 2
            centery = sizey / 2

            strOutFile = imgname +"-ra-ps.csv"
            strRotAvg = imgname + "-ra-ps"

            dst := CreateFloatImage( "dst", halfMinor, samples )
            k = 2 * pi() / samples
            dst = warp( theMod, icol*sin(irow*k) + centerx, icol*cos(irow*k) + centery )

         }
         line_projection := CreateFloatImage( strRotAvg, halfMinor, 1 )
         line_projection = 0
         line_projection[icol,0] += dst
         line_projection /= samples

         ImageSetDimensionCalibration( line_projection, 0 , 0.0, dDeltaS, "1/Å", 1 )

         if(g_bSaveCsvFile)
         {
            if(SaveAsDialog( "Save Profile", strOutFile, strOutFile ))
            {
              nFile = CreateFileForWriting(strOutFile )
              WriteFile( nFile, 0, "|s| [1/Å], I\n" )
              for( i = 0; i < halfMinor; ++i )
              {
                  dS = i * dDeltaS
                  dI = GetPixel(line_projection, i, 0)
                  SetPixel(line_projection, i, 0, log(dI+1))
                  WriteFile( nFile, 0, dS + "," + (dI/dIntFactor) + "\n" )
              }
              CloseFile( nFile )
            }
         }

         if (g_bShowLinePlot)
         {
            ShowImage(line_projection)
         }
         else
         {
            deleteimage(line_projection)
         }
         return
   }
}

// Get desired defaults and store in global variables
number bRet
bRet = GetPersistentNumberNote("Periodogram:CropInnerRadius", g_nCropInnerRadius)
if (bRet < 1)
{
   g_nCropInnerRadius = 2
   SetPersistentNumberNote("Periodogram:CropInnerRadius", g_nCropInnerRadius)
}

bRet = GetPersistentNumberNote("Periodogram:SizeFFT", g_nFFTsize)
if (bRet < 1)
{
   g_nFFTsize = 512
   SetPersistentNumberNote("Periodogram:SizeFFT", g_nFFTsize)
}

bRet = GetPersistentNumberNote("Periodogram:Overlap", g_nOverlap)
if (bRet < 1)
{
   g_nOverlap = 0
   SetPersistentNumberNote("Periodogram:Overlap", g_nOverlap)
}

bRet = GetPersistentNumberNote("Periodogram:Gamma", g_nGamma)
if (bRet < 1)
{
   g_nGamma = 0.5
   SetPersistentNumberNote("Periodogram:Gamma", g_nGamma)
}

bRet = GetPersistentNumberNote("Periodogram:MaxLimitFr", g_nMaxLimitFr)
if (bRet < 1)
{
   g_nMaxLimitFr = 1.0
   SetPersistentNumberNote("Periodogram:MaxLimitFr", g_nGamma)
}

bRet = GetPersistentNumberNote("Periodogram:CropCenter", g_bCropCenter)
if (bRet < 1)
{
   g_bCropCenter = 1
   SetPersistentNumberNote("Periodogram:CropCenter", g_bCropCenter)
}

bRet = GetPersistentNumberNote("Periodogram:UseSqrt", g_bUseSqrt)
if (bRet < 1)
{
   g_bUseSqrt = 1
   SetPersistentNumberNote("Periodogram:UseSqrt", g_bUseSqrt)
}

bRet = GetPersistentNumberNote("Periodogram:LimitHalfNyquist", g_bLimitHalfNyquist)
if (bRet < 1)
{
   g_bLimitHalfNyquist = 1
   SetPersistentNumberNote("Periodogram:LimitHalfNyquist", g_bLimitHalfNyquist)
}

bRet = GetPersistentNumberNote("Periodogram:SaveCsvFile",  g_bSaveCsvFile)
if (bRet < 1)
{
    g_bSaveCsvFile = 1
   SetPersistentNumberNote("Periodogram:SaveCsvFile",  g_bSaveCsvFile)
}

bRet = GetPersistentNumberNote("Periodogram:ShowLinePlot", g_bShowLinePlot)
if (bRet < 1)
{
   g_bShowLinePlot = 1
   SetPersistentNumberNote("Periodogram:ShowLinePlot", g_bShowLinePlot)
}


// be sure we have a results window open...
OpenResultsWindow()


// Create Dialog
PDT_Dlg = DLGCreateDialog( "PDTool",  PDT_DlgItems )

// create fields
PDT_CropInnerRadiusField     = DLGCreateIntegerField("     Crop inner radius:", PDT_CropInnerRadius, g_nCropInnerRadius, 10)
PDT_FFTsizeField             = DLGCreateIntegerField("              FFT Size:", PDT_FFTsize, g_nFFTsize, 10)
PDT_OverlapField             = DLGCreateIntegerField("          Overlap [px]:", PDT_Overlap, g_nOverlap, 10)
PDT_GammaField               = DLGCreateRealField   ("                 Gamma:", PDT_Gamma, g_nGamma, 10,2)
PDT_MaxLimitFrField          = DLGCreateRealField   ("          Max Limit Fr:", PDT_MaxLimitFr, g_nMaxLimitFr, 10,2)

// create boxes
PDT_CropCenterBox            = DLGCreateCheckBox("Crop Center ?          ", g_bCropCenter)
PDT_LimitHalfNyquistBox      = DLGCreateCheckBox("Limit to half Nyquist? ", g_bLimitHalfNyquist)
PDT_UseSqrtBox               = DLGCreateCheckBox("Use Sqrt Intens?       ", g_bUseSqrt)
PDT_SaveCsvBox               = DLGCreateCheckBox("Save CSV file?         ", g_bSaveCsvFile)
PDT_ShowLinePlotBox          = DLGCreateCheckBox("Show Line Plot?        ", g_bShowLinePlot)
// create button
PDT_ComputePeriodogramButton = DLGCreatePushButton("  Compute periodogram  ", "compute_periodogram")

// Add items to dialog & define the layout (1 column, 14 rows)
PDT_Dlg.DLGAddElement(PDT_Label1)
PDT_Dlg.DLGAddElement(PDT_Label2)
PDT_Dlg.DLGAddElement(PDT_CropInnerRadiusField)
PDT_Dlg.DLGAddElement(PDT_FFTsizeField)
PDT_Dlg.DLGAddElement(PDT_OverlapField)
PDT_Dlg.DLGAddElement(PDT_Label3)
PDT_Dlg.DLGAddElement(PDT_GammaField)
PDT_Dlg.DLGAddElement(PDT_MaxLimitFrField)


PDT_Dlg.DLGAddElement(PDT_CropCenterBox)
PDT_Dlg.DLGAddElement(PDT_UseSqrtBox)
PDT_Dlg.DLGAddElement(PDT_LimitHalfNyquistBox)
PDT_Dlg.DLGAddElement(PDT_SaveCsvBox)
PDT_Dlg.DLGAddElement(PDT_ShowLinePlotBox)

PDT_Dlg.DLGAddElement(PDT_ComputePeriodogramButton)

PDT_Dlg.DLGTableLayout(1,14,0)

objPDToolWindow = alloc( PDTool).Init(PDT_Dlg)
objPDToolWindow.Display("Periodogram")
