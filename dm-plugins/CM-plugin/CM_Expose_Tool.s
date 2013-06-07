// Script to automate recording of low dose and images at a specified 
// defocus by DM on a CM microscope. Requires EMControl.
//
// Tested under DM 1.70.16
//
// CM_Expose_Tool
//
// Created JRM 29-May-2008
// 
// Modifcation History:
//
//   Date        Who   What...
// -----------   ---   ----------------------------------------------------------
// 29-May-2008   JRM   Initial prototype

TagGroup CMET_Dlg, CMET_DlgItems;

Taggroup CMET_ExpTime, CMET_ExpTimeField;
Taggroup CMET_DelayTime, CMET_DelayTimeField;
Taggroup CMET_DACtoNm, CMET_DACtoNmField;

TagGroup CMET_DefocusLabel;
Taggroup CMET_DefocusNm, CMET_DefocusNmField;
Taggroup CMET_DefocusOffsetNm, CMET_DefocusOffsetNmField;

Taggroup CMET_RecdLowDoseButton, CMET_RecdDefocusButton;
Object   objCMExposeToolWindow;

number CMET_fExpose, CMET_fDelay, CMET_fFocusDacCalib, CMET_fDefocusNm, CMET_fDefocusOffsetNm;

number CMET_FocusToDac( number nDefocusNm)
{
   // Compute the number of DAC steps to achieve defocus
 
   number nDacUnits;                  // step size in DAC units
   
   nDacUnits = Round( nDefocusNm / CMET_fFocusDacCalib);

  return nDacUnits;
}

number CMET_SetSearchMode()
{
   number nRet;
   number nSearchKey = 6;
   number nPresses = 1;
   nRet =  CMPressSoftKey(nSearchKey, nPresses );
   return nRet;
}

number CMET_SetFocusMode()
{
   number nRet;
   number nFocusKey  = 5;
   number nPresses = 1;
   nRet =  CMPressSoftKey(nFocusKey, nPresses );
   return nRet;
}

number CMET_SetExposeMode()
{
   number nRet;
   number nExposeKey = 4;
   number nPresses = 1;
   nRet =  CMPressSoftKey(nExposeKey, nPresses );
   return nRet;
}

// This bit of code is where buttons and pulldowns generate responses.
class CMExposeTool : uiframe
{

  void record_low_dose_image(object self)
  {
     number nHardware = 1; // set to > 0 if we really have a camera
     number nTop, nLeft, nCcdSize;
     number nDacUnits, nTicks, bRet;
     number dMag;

     nTop = 0;
     nLeft = 0;
     nCcdSize = 2048;

     // get values from DLG and save
     CMET_fExpose = CMET_ExpTime.DLGGetValue();
     SetPersistentNumberNote("CM:ExpTimeSec", CMET_fExpose);

     CMET_fDelay = CMET_DelayTime.DLGGetValue();
     SetPersistentNumberNote("CM:DelayTimeSec", CMET_fDelay);

     CMET_fFocusDacCalib = CMET_DACtoNm.DLGGetValue();
     SetPersistentNumberNote("CM:FocusDACtoNM", CMET_fFocusDacCalib);

     CMET_fDefocusNm = CMET_DefocusNm.DLGGetValue();
     SetPersistentNumberNote("CM:DefocusNm", CMET_fDefocusNm);

     CMET_fDefocusOffsetNm = CMET_DefocusOffsetNm.DLGGetValue();
     SetPersistentNumberNote("CM:DefocusOffsetNm", CMET_fDefocusOffsetNm);
     
     nDacUnits = CMET_FocusToDac( CMET_fDefocusNm - CMET_fDefocusOffsetNm);
     nTicks = Round(1000. * CMET_fDelay);

     bRet = CMET_SetExposeMode();
      
     // let's double check the mag
     dMag = CM( );
     SetPersistentNumberNote("Microscope Info:Indicated Magnification", dMag);
           
     EMChangeFocus(nDacUnits);
     Delay(nTicks);
     image  imgResult := SSCGainNormalizedAcquire( CMET_fExpose, nTop, nLeft, nCcdSize, nCcdSize );
     ShowImage(imgResult);                
     EMChangeFocus(-nDacUnits);
            
     bRet = CMET_SetFocusMode();
     TagGroup tg = imgResult.ImageGetTagGroup();
     SetNumberNote( imgResult, "Microscope Info:Defocus_nm", CMET_fDefocusNm);
     Result("The image was recorded with a defocus of " + CMET_fDefocusNm + " [nm].\n" );   
	
    return;   
  }
  
  void record_defocus_image(object self)
  {
     number nHardware = 1; // set to > 0 if we really have a camera
     number nTop, nLeft, nCcdSize;
     number nDacUnits, bRet, nDefocusMicrons;
     number dMag;

     nTop = 0;
     nLeft = 0;
     nCcdSize = 2048;

     // get values from DLG and save
     CMET_fExpose = CMET_ExpTime.DLGGetValue();
     SetPersistentNumberNote("CM:ExpTimeSec", CMET_fExpose);

     CMET_fFocusDacCalib = CMET_DACtoNm.DLGGetValue();
     SetPersistentNumberNote("CM:FocusDACtoNM", CMET_fFocusDacCalib);

     CMET_fDefocusNm = CMET_DefocusNm.DLGGetValue();
     SetPersistentNumberNote("CM:DefocusNm", CMET_fDefocusNm);

     
     nDacUnits = CMET_FocusToDac( CMET_fDefocusNm );
    
     // let's double check the mag
     dMag = CM( );
     SetPersistentNumberNote("Microscope Info:Indicated Magnification", dMag);
           
     EMChangeFocus(nDacUnits);
     image  imgResult := SSCGainNormalizedAcquire( CMET_fExpose, nTop, nLeft, nCcdSize, nCcdSize );
     ShowImage(imgResult);                
     EMChangeFocus(-nDacUnits);
            
     TagGroup tg = imgResult.ImageGetTagGroup();
     SetNumberNote( imgResult, "Microscope Info:Defocus_nm", CMET_fDefocusNm);
     Result("The image was recorded with a defocus of " + CMET_fDefocusNm + " [nm].\n" ); 
	
     return;   
  }
}


// Get desired defaults
number bRet;
bRet = GetPersistentNumberNote("CM:ExpTimeSec", CMET_fExpose);
if (bRet < 1)
{
   CMET_fExpose = 1.0;
   SetPersistentNumberNote("CM:ExpTimeSec", CMET_fExpose);
}

bRet = GetPersistentNumberNote("CM:DelayTimeSec", CMET_fDelay);
if (bRet < 1)
{
   CMET_fDelay = 0.5;
   SetPersistentNumberNote("CM:DelayTimeSec", CMET_fDelay);
}

bRet = GetPersistentNumberNote("CM:FocusDACtoNM", CMET_fFocusDacCalib);
if (bRet < 1)
{
   CMET_fFocusDacCalib = 0.003889;
   SetPersistentNumberNote("CM:FocusDACtoNM", CMET_fFocusDacCalib);
}


bRet = GetPersistentNumberNote("CM:DefocusNm", CMET_fDefocusNm);
if (bRet < 1)
{
   CMET_fDefocusNm = -90.1;
   SetPersistentNumberNote("CM:DefocusNm", CMET_fDefocusNm);
}


bRet = GetPersistentNumberNote("CM:DefocusOffsetNm", CMET_fDefocusOffsetNm);
if (bRet < 1)
{
   CMET_fDefocusOffsetNm = 0;
   SetPersistentNumberNote("CM:DefocusOffsetNm", CMET_fDefocusOffsetNm);
}


// be sure we have a results window open...
OpenResultsWindow();


// Create Dialog
CMET_Dlg = DLGCreateDialog( "CMExposeTool", CMET_DlgItems );

// create label
CMET_DefocusLabel = DLGCreateLabel( "Defocus: " );

// create fields
CMET_ExpTimeField         = DLGCreateRealField("      Exp time [sec]:", CMET_ExpTime, CMET_fExpose, 10, 3);
CMET_DelayTimeField       = DLGCreateRealField("    Delay time [sec]:", CMET_DelayTime, CMET_fDelay, 10, 3);
CMET_DACtoNmField         = DLGCreateRealField("Focus Calib [nm/DAC]:", CMET_DACtoNm, CMET_fFocusDacCalib, 10, 6);
CMET_DefocusNmField       = DLGCreateRealField("        Defocus [nm]:", CMET_DefocusNm, CMET_fDefocusNm, 10, 2);
CMET_DefocusOffsetNmField = DLGCreateRealField(" Defocus Offset [nm]:", CMET_DefocusOffsetNm, CMET_fDefocusOffsetNm, 10, 2);

// create buttons
CMET_RecdLowDoseButton = DLGCreatePushButton( "Rec Low Dose Image", "record_low_dose_image");
CMET_RecdDefocusButton = DLGCreatePushButton( " Rec Defocus Image", "record_defocus_image");

// Add items to dialog & define the layout (1 columns, 7 rows)
CMET_Dlg.DLGAddElement(CMET_DACtoNmField);
CMET_Dlg.DLGAddElement(CMET_DelayTimeField);
CMET_Dlg.DLGAddElement(CMET_ExpTimeField);
CMET_Dlg.DLGAddElement(CMET_DefocusOffsetNmField);
CMET_Dlg.DLGAddElement(CMET_DefocusNmField);

CMET_Dlg.DLGAddElement(CMET_RecdLowDoseButton);
CMET_Dlg.DLGAddElement(CMET_RecdDefocusButton);

CMET_Dlg.DLGTableLayout(1,7,0);



objCMExposeToolWindow = alloc( CMExposeTool).Init(CMET_Dlg);
objCMExposeToolWindow.Display("CMExposeTool");




