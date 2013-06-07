// Script to permit easy setting of CompuStage X & Y from
// DM. Requires EMControl. Especially useful to toggle
// Alpha tilt to set eucentric position
//
// Tested under DM 1.82.366
//
//
// Created JRM 27-May-2008
// 
// Modifcation History:
//
//   Date        Who   What...
// -----------   ---   ----------------------------------------------------------
// 28-Sep-2010   JRM   Initial prototype
// 10-Apr-2013   JRM   Added Z coordinate

TagGroup CompustageDlg, CompustageDlgItems;
Taggroup StageXcoord, StageXcoordField, SetStageXcoordButton, GetStageXcoordButton;
Taggroup StageYcoord, StageYcoordField, SetStageYcoordButton, GetStageYcoordButton;
Taggroup StageZcoord, StageZcoordField, SetStageZcoordButton, GetStageZcoordButton;
Taggroup CoordPt, CoordPtField, CoordPtToFileButton, CoordPtFromFileButton;
Object   objStageCoordWindow;
number   fStageXcoordVal, fStageYcoordVal, fStageZcoordVal, nFile;
string   strPoint, strFile, strLine;


// This bit of code is where buttons and pulldowns generate responses.
class CMStageCoordTool : uiframe
{
  void set_z_coord(object self)
  {
     fStageZcoordVal = StageZcoord.DLGGetValue();
     SetPersistentNumberNote("CM:StageZcoord", fStageZcoordVal);
     EMSetStageZ(fStageZcoordVal);
  }

  void get_z_coord(object self)
  {
    fStageZcoordVal = EMGetStageZ();
	SetPersistentNumberNote("CM:StageZcoord", fStageZcoordVal);
	StageZcoord.DLGValue(fStageZcoordVal)
	
  }

  void set_y_coord(object self)
  {
     fStageYcoordVal = StageYcoord.DLGGetValue();
     SetPersistentNumberNote("CM:StageYcoord", fStageYcoordVal);
     EMSetStageY(fStageYcoordVal);
  }

  void get_y_coord(object self)
  {
    fStageYcoordVal = EMGetStageY();
	SetPersistentNumberNote("CM:StageYcoord", fStageYcoordVal);
	StageYcoord.DLGValue(fStageYcoordVal)
	
  }

  void set_x_coord(object self)
  {
     fStageXcoordVal = StageXcoord.DLGGetValue();
     SetPersistentNumberNote("CM:StageXcoord", fStageXcoordVal);
     EMSetStageX(fStageXcoordVal);
  }

  void get_x_coord(object self)
  {
    fStageXcoordVal = EMGetStageX();
	SetPersistentNumberNote("CM:StageXcoord", fStageXcoordVal);
	StageXcoord.DLGValue(fStageXcoordVal);
  }
  
  void pt_to_file(object self)
  {
	// read values from the dialog
	 fStageXcoordVal = StageXcoord.DLGGetValue();
	 fStageYcoordVal = StageYcoord.DLGGetValue();
	 fStageZcoordVal = StageZcoord.DLGGetValue();
     DLGGetValue(CoordPt, strPoint);
     SetPersistentStringNote("CM:Point", strPoint);
     
     // make certain the directory for storing coordinates exists
     CreateDirectory("c:\\data");
	 CreateDirectory("c:\\data\\atd");
	 CreateDirectory("c:\\data\\atd\\coords");
	 
	 strFile = "c:\\data\\atd\\coords\\" + strPoint + ".txt";
	 // result("File = " + strFile + "\n");
	 nFile =  CreateFileForWriting( strFile );
	 
	 // result("nFile = " + nFile + "\n")
	 if (nFile > 1)	 
	{
		strLine = Format(fStageXcoordVal,"%10.3f")
		WriteFile( nFile, strLine );		
		WriteFile( nFile, "\n" );
		
		strLine = Format(fStageYcoordVal,"%10.3f")
		WriteFile( nFile, strLine );
		WriteFile( nFile, "\n" );
		
		strLine = Format(fStageZcoordVal,"%10.3f")
		WriteFile( nFile, strLine );
		WriteFile( nFile, "\n" );
		
		CloseFile( nFile );
	}
	else
	{
		Result("Didn't successfully write the point file");
	
	}
     
  }

  void pt_from_file(object self)
  {
    DLGGetValue(CoordPt, strPoint);
    SetPersistentStringNote("CM:Point", strPoint);
	strFile = "c:\\data\\atd\\coords\\" + strPoint + ".txt";
	nFile = OpenFileForReading( strFile );
	// result("nFile = " + nFile + "\n")
	if (nFile > 1)
	{
		readfileline(nFile, strLine);
		fStageXcoordVal = val(strLine);
		SetPersistentNumberNote("CM:StageXcoord", fStageXcoordVal);
		StageXcoord.DLGValue(fStageXcoordVal)
		
		readfileline(nFile, strLine);
		fStageYcoordVal = val(strLine);
		SetPersistentNumberNote("CM:StageYcoord", fStageYcoordVal);
		StageYcoord.DLGValue(fStageYcoordVal);
		
		readfileline(nFile, strLine);
		fStageZcoordVal = val(strLine);
		SetPersistentNumberNote("CM:StageZcoord", fStageZcoordVal);
		StageZcoord.DLGValue(fStageZcoordVal);
		
		CloseFile( nFile );
	}
	else
	{
		Result("Didn't successfully read the point file");
	
	}
	
	
  }
}


// Get desired defaults
number bRet

bRet = GetPersistentNumberNote("CM:StageXcoord", fStageXcoordVal);
if (bRet < 1)
{
      fStageXcoordVal = 0;
      SetPersistentNumberNote("CM:StageXcoord", fStageXcoordVal);
}

bRet = GetPersistentNumberNote("CM:StageYcoord", fStageYcoordVal);
if (bRet < 1)
{
      fStageYcoordVal = 0;
      SetPersistentNumberNote("CM:StageYcoord", fStageYcoordVal);
}

bRet = GetPersistentNumberNote("CM:StageZcoord", fStageZcoordVal);
if (bRet < 1)
{
      fStageZcoordVal = 0;
      SetPersistentNumberNote("CM:StageZcoord", fStageZcoordVal);
}

bRet = GetPersistentStringNote("CM:Point", strPoint);
if (bRet < 1)
{
      strPoint = "Point1";
      SetPersistentStringNote("CM:Point", strPoint);
}


// Create Dialog
CompustageDlg     = DLGCreateDialog( "CMStageTool", CompustageDlgItems );


// Create items
StageXcoordField  = DLGCreateRealField("Stage X [µm]:", StageXcoord, fStageXcoordVal, 10,4);
GetStageXcoordButton = DLGCreatePushButton( "Get X", "get_x_coord");
SetStageXcoordButton = DLGCreatePushButton( "Set X", "set_x_coord");


StageYcoordField  = DLGCreateRealField("Stage Y [µm]:", StageYcoord, fStageYcoordVal, 10,4);
GetStageYcoordButton = DLGCreatePushButton( "Get Y", "get_y_coord");
SetStageYcoordButton = DLGCreatePushButton( "Set Y", "set_y_coord");

StageZcoordField  = DLGCreateRealField("Stage Z [µm]:", StageZcoord, fStageZcoordVal, 10,4);
GetStageZcoordButton = DLGCreatePushButton( "Get Z", "get_z_coord");
SetStageZcoordButton = DLGCreatePushButton( "Set Z", "set_z_coord");


CoordPtField  = DLGCreateStringField("Point Name:", CoordPt, strPoint, 20);
CoordPtToFileButton = DLGCreatePushButton( "To File", "pt_to_file");
CoordPtFromFileButton = DLGCreatePushButton( "From File", "pt_from_file");

// Add items to dialog & define the layout (3 columns, 3 rows)
CompustageDlg.DLGAddElement(StageXcoordField)
CompustageDlg.DLGAddElement(GetStageXcoordButton)
CompustageDlg.DLGAddElement(SetStageXcoordButton)

CompustageDlg.DLGAddElement(StageYcoordField)
CompustageDlg.DLGAddElement(GetStageYcoordButton)
CompustageDlg.DLGAddElement(SetStageYcoordButton)

CompustageDlg.DLGAddElement(StageZcoordField)
CompustageDlg.DLGAddElement(GetStageZcoordButton)
CompustageDlg.DLGAddElement(SetStageZcoordButton)

CompustageDlg.DLGAddElement(CoordPtField)
CompustageDlg.DLGAddElement(CoordPtToFileButton)
CompustageDlg.DLGAddElement(CoordPtFromFileButton)


CompustageDlg.DLGTableLayout(3,4,0)


objStageCoordWindow = alloc(CMStageCoordTool).Init(CompustageDlg);
objStageCoordWindow.Display("CMStageCoordTool")



