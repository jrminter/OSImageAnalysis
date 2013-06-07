// Script to permit easy setting of stage tilts from
// DM. Requires EMControl. Especially useful to toggle
// Alpha tilt to set eucentric position
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

TagGroup StageTiltDlg, StageTiltDlgItems;
Taggroup AlphaTilt, AlphaTiltField, AlphaTiltButton, AlphaZeroButton;
Taggroup BetaTilt, BetaTiltField, BetaTiltButton, BetaZeroButton;
Object   objStageTiltWindow;
number fAlphaVal, fBetaVal;


// This bit of code is where buttons and pulldowns generate responses.
class CMStageTiltTool : uiframe
{

  void tilt_to_beta(object self)
  {
     fBetaVal = BetaTilt.DLGGetValue();
     SetPersistentNumberNote("CM:BetaDeg", fBetaVal);
     EMSetStageBeta(fBetaVal);
  }

  void zero_beta(object self)
  {
    EMSetStageBeta(0);
  }

  void tilt_to_alpha(object self)
  {
     fAlphaVal = AlphaTilt.DLGGetValue();
     SetPersistentNumberNote("CM:AlphaDeg", fAlphaVal);
     EMSetStageAlpha(fAlphaVal);
  }

  void zero_alpha(object self)
  {
     EMSetStageAlpha(0);

  }
}


// Get desired defaults
number bRet

bRet = GetPersistentNumberNote("CM:AlphaDeg", fAlphaVal);
if (bRet < 1)
{
      fAlphaVal = 12;
      SetPersistentNumberNote("CM:AlphaDeg", fAlphaVal);
}

bRet = GetPersistentNumberNote("CM:BetaDeg", fBetaVal);
if (bRet < 1)
{
      fBetaVal = 2;
      SetPersistentNumberNote("CM:BetaDeg", fBetaVal);
}


// Create Dialog
StageTiltDlg     = DLGCreateDialog( "CMStageTool", StageTiltDlgItems );


// Create items
AlphaTiltField  = DLGCreateRealField("Alpha Tilt [deg]:", AlphaTilt, fAlphaVal, 10,3);
AlphaTiltButton = DLGCreatePushButton( "Alpha -> t", "tilt_to_alpha");
AlphaZeroButton = DLGCreatePushButton( "Alpha -> 0", "zero_alpha");


BetaTiltField  = DLGCreateRealField("Beta Tilt [deg]:", BetaTilt, fBetaVal, 10,3);
BetaTiltButton = DLGCreatePushButton( "Beta -> t", "tilt_to_beta");
BetaZeroButton = DLGCreatePushButton( "Beta -> 0", "zero_beta");

// Add items to dialog & define the layout (3 columns, 2 rows)
StageTiltDlg.DLGAddElement(AlphaTiltField)
StageTiltDlg.DLGAddElement(AlphaTiltButton)
StageTiltDlg.DLGAddElement(AlphaZeroButton)

StageTiltDlg.DLGAddElement(BetaTiltField)
StageTiltDlg.DLGAddElement(BetaTiltButton)
StageTiltDlg.DLGAddElement(BetaZeroButton)


StageTiltDlg.DLGTableLayout(3,2,0)


objStageTiltWindow = alloc(CMStageTiltTool).Init(StageTiltDlg);
objStageTiltWindow.Display("CMStageTiltTool")



