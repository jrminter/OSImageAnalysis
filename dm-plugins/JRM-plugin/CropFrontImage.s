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
// 2013-05-29    JRM   Use - instaead of _ in names


void CropFrontImage(void)
{
   image imgFront, imgCrop;
   number nScaleX, nScaleY;
   string szUnits, szName;

   imgFront := GetFrontImage();
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

CropFrontImage();
