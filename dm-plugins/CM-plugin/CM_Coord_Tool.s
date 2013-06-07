// Script to provide a window with a button to
// get coordinates and focus and store to a
// tag group in the front image
// Requires EMControl.
//
// Tested under DM 1.70.16
//
//
// Created JRM 27-May-2008
// 
// Modifcation History:
//
//   Date        Who   What...
// -----------   ---   ----------------------------------------------------------
// 27-May-2008   JRM   Initial prototype

TagGroup CoordToolDlg, CoordToolDlgItems;
Taggroup GetCoordButton, CoordToolLabel;
Object   objCoordToolWindow;

TagGroup GetStageToTagGroup(void)
{

   TagGroup tgStageCM = NewTagGroup();
   number index, bRet, fFocusDacCalib, fDeltaNm;
   
   bRet = GetPersistentNumberNote("CM:FocusDACtoNM", fFocusDacCalib);
   if (bRet < 1)
   {
      fFocusDacCalib = 2.39;
      SetPersistentNumberNote("CM:FocusDACtoNM", fFocusDacCalib);
   }

  
   index = tgStageCM.TagGroupCreateNewLabeledTag( "X [µm]" ); 
   number nStageX = EMGetStageX();
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nStageX );
   Result("       X: " + nStageX + " [µm]\n");

   index = tgStageCM.TagGroupCreateNewLabeledTag( "Y [µm]" );  
   number nStageY = EMGetStageY();
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nStageY );
   Result("       Y: " + nStageY + " [µm]\n");


   index = tgStageCM.TagGroupCreateNewLabeledTag( "Z [µm]" ); 
   number nStageZ = EMGetStageZ();
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nStageZ );
   Result("       Z: " + nStageZ + " [µm]\n");

   index = tgStageCM.TagGroupCreateNewLabeledTag( "Alpha [deg]" ); 
   number nStageAlpha = EMGetStageAlpha();
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nStageAlpha );
   Result("   Alpha: " + nStageAlpha + " [°]\n");


   index = tgStageCM.TagGroupCreateNewLabeledTag( "Beta [deg]" ); 
   number nStageBeta = EMGetStageBeta();
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nStageBeta );
   Result("    Beta: " + nStageBeta + " [°]\n");

   index = tgStageCM.TagGroupCreateNewLabeledTag( "OL DAC units from Preset" );
   number nDacUnits = EMgetFocus();
   tgStageCM.TagGroupSetIndexedTagAsLong( index, nDacUnits );
   Result("DeltaDAC: " + nDacUnits + " [DAC Units]\n");

   index = tgStageCM.TagGroupCreateNewLabeledTag( "OL nm from Preset" );
   fDeltaNm = nDacUnits * fFocusDacCalib;
   tgStageCM.TagGroupSetIndexedTagAsFloat( index, nDacUnits );
   Result(" DeltaOL: " + fDeltaNm + " [nm]\n");



   return tgStageCM;
}

void AddStageTagsToFrontImage (void)
{
   TagGroup tgTest;
   image imFront := GetFrontImage();
   String strName = GetName(imFront);
   Result("\n\n");
   Result(strName);
   Result("\n");   
   TagGroup tgStage = GetStageToTagGroup();
   TagGroup tgImage = ImageGetTagGroup(imFront);
   if(tgImage.TagGroupGetTagAsTagGroup( "Stage Coordinates", tgTest ) )
   {
      TagGroupDeleteTagWithLabel(tgImage, "Stage Coordinates" );

   }
   TagGroupAddLabeledTagGroup( tgImage, "Stage Coordinates", tgStage );
}


// This bit of code is where buttons and pulldowns generate responses.
class CMCoordTool : uiframe
{

  void get_coordinates(object self)
  {
     AddStageTagsToFrontImage();     
  }
}

// be sure we have a results window open...
OpenResultsWindow();

// Create Dialog
CoordToolDlg = DLGCreateDialog( "CMCoordTool", CoordToolDlgItems );

// create label
CoordToolLabel = DLGCreateLabel( "At start of session 1) Press Auto Focus preset, 2) Press reset defocus,\n 3) Normalize lenses. Then use this to store coordinates to active image" ) 

// Create button
GetCoordButton  = DLGCreatePushButton( "Get coordinates to active image", "get_coordinates");



// Add items to dialog & define the layout (1 columns, 2 rows)
CoordToolDlg.DLGAddElement(CoordToolLabel)
CoordToolDlg.DLGAddElement(GetCoordButton)

CoordToolDlg.DLGTableLayout(1,2,0)


objCoordToolWindow = alloc(CMCoordTool).Init(CoordToolDlg);
objCoordToolWindow.Display("CMCoordTool")



