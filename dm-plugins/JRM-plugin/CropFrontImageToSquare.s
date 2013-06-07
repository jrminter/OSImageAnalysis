// Script to crop a ROI from the front image
// by J. R. Minter
// 
// Modifcation History:
//
//   Date        Who   What...
// -----------   ---   -------------------------------------------
// 2007-10-26    JRM   Initial version 1.0
// 2007-11-26    JRM   Copy kV, Mag, and Cs
// 2008-11-03    JRM   new naming convention
// 2008-12-02    JRM   new version to crop a square around a point
// 2013-05-29    JRM   replace _ in name with -

ROI GetOrCreateCropPoint( Image img )
{
   ImageDisplay imgDisp
   Try imgDisp = img.ImageGetImageDisplay(0) Catch Throw("No image found")

   ROI r

   Number ROI_count = imgDisp.ImageDisplayCountROIs()
   Number w, h, ROI_w, ROI_h, cx, cy, bRet

   Number ROI_Found = 0

   //	find a point ROI which is selected
 
   for( number i = ROI_Count-1;i>=0; i--) // check to see there is any point ROI and if it is selected
   {
      r = imgDisp.ImageDisplayGetROI(i)

      If( r.ROIIsPoint() && imgDisp.ImageDisplayIsROISelected(r) )
      {
         ROI_Found =1
         i = -1
      }
      ELSE if( r.ROIIsPoint() )
      {
         ROI_Found = 1
         i=-1
      }
   }

   If( !ROI_Found ) // create a point ROI if there is not any ROI present
   {
      img.GetSize(w, h)
      r = CreateROI()
      bRet = GetPersistentNumberNote("CropToSquare:CenterX", cx);
      if (bRet < 1)
      {
         cx = w/2;  // set to middle
         SetPersistentNumberNote("CropToSquare:CenterX", cx);
      }

      bRet = GetPersistentNumberNote("CropToSquare:CenterY", cy);
      if (bRet < 1)
      {
         cy = h/2;  // set to middle
         SetPersistentNumberNote("CropToSquare:CenterY", cy);
      }
         
      r.ROISetPoint( cx, cy )
      imgDisp.ImageDisplayAddROI(r)
      imgDisp.ImageDisplaySetROIselected(r,1)
   }
   
   // let's save the coordinates, whatever they are
   ROIGetPoint(r, cx, cy );
   SetPersistentNumberNote("CropToSquare:CenterX", cx);
   SetPersistentNumberNote("CropToSquare:CenterY", cy);

   r.ROISetVolatile(1)  // set ROI to be non-volatile

   return r
}


void CropFrontImageToSquare(void)
{
   image imgFront, imgCrop;
   number nScaleX, nScaleY, nHalf;
   number nX, nY, nTop, nLeft, nBottom, nRight, bRet
   string szUnits, szName;

   imgFront := GetFrontImage();
   ROI rPoint = imgFront.GetOrCreateCropPoint();
   ROIGetPoint(rPoint, nX, nY );
   bRet = GetPersistentNumberNote("CropToSquare:HalfSize", nHalf);
   if (bRet < 1)
   {
      nHalf = 256
      
   }
   bRet = GetNumber( "Enter half size",  nHalf,  nHalf );
   if (bRet > 0)
   {
      SetPersistentNumberNote("CropToSquare:HalfSize",  nHalf);
   }
   nLeft   = nX - nHalf
   nRight  = nX + nHalf
   nTop    = nY - nHalf
   nBottom = nY + nHalf
   ImageDisplay dspFront
   Try dspFront = imgFront.ImageGetImageDisplay(0) Catch Throw("No image found")
   dspFront.ImageDisplayDeleteROI( rPoint ) 
   
   ROI rCrop = NewROI( )
   rCrop.ROISetRectangle( nTop, nLeft, nBottom, nRight )
   
   dspFront.ImageDisplayAddROI( rCrop )  
 

   
   imgCrop = imgFront[];

   TagGroup	tgImgParams = imgFront.ImageGetTagGroup();
   number nMag;
   tgImgParams.TagGroupGetTagAsNumber( "Microscope Info:Indicated Magnification", nMag );
   number nVoltage;
   tgImgParams.TagGroupGetTagAsNumber( "Microscope Info:Voltage", nVoltage );
   number nCs;
   tgImgParams.TagGroupGetTagAsNumber( "Microscope Info:Cs(mm)", nCs );

   getscale(imgFront, nScaleX, nScaleY);
   getunitstring(imgFront, szUnits);
   getname(imgFront, szName);

   setscale(imgCrop, nScaleX, nScaleY)
   setunitstring(imgCrop, szUnits);
   SetName(imgCrop, szName + "-cr");
   tgImgParams = imgCrop.ImageGetTagGroup();
   tgImgParams.TagGroupSetTagAsNumber( "Microscope Info:Indicated Magnification", nMag );
   tgImgParams.TagGroupSetTagAsNumber( "Microscope Info:Voltage", nVoltage );
   tgImgParams.TagGroupSetTagAsNumber( "Microscope Info:Cs(mm)", nCs );

   ShowImage(imgCrop); 
}

CropFrontImageToSquare();
