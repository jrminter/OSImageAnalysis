// Script to permit timely adjustment of the cathode
// DM. Requires EMControl. Especially useful to not
// shock a LaB6 cathode
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

TagGroup CathodeDlg, CathodeDlgItems;
Taggroup SatCathodeSteps, SatCathodeStepsField;
Taggroup SatCathodeWait, SatCathodeWaitField;
Taggroup DesatCathodeWait, DesatCathodeWaitField;
Taggroup SatCathodeButton, DesatCathodeButton;
Object   objCathodeWindow;
number nSatSteps, nSatWait, nDesatWait;

void CMCT_WaitSecs(number nSec)
{
   number nTicks = 60. * nSec;
   Delay(nTicks);
}

void BringUpCathode( number nMaxSteps, number nDelaySecs)
{
   number i;
   number iFilamentKnob = 17;
   for(i=0; i < nMaxSteps; ++i)
   {
      CMTurnKnob( iFilamentKnob, 1 );
      Result("step " + (i+1) + " of " + nMaxSteps + "\n" ); 
      CMCT_WaitSecs(nDelaySecs);       
   }
}

void BringDownCathode( number nMaxSteps, number nDelaySecs)
{
   number i;
   number iFilamentKnob = 17;
   for(i=0; i < nMaxSteps; ++i)
   {
      CMTurnKnob( iFilamentKnob, -1 );
      Result("step " + (i+1) + " of " + nMaxSteps + "\n" );  
      CMCT_WaitSecs(nDelaySecs);    
   }
}


// This bit of code is where buttons and pulldowns generate responses.
class CMCathodeTool : uiframe
{

  void saturate_cathode(object self)
  {
     number nMin;
     nSatWait = SatCathodeWait.DLGGetValue();
     nSatSteps = SatCathodeSteps.DLGGetValue();
     nMin = nSatSteps * nSatWait / 60;
     SetPersistentNumberNote("CM:CathSatWait", nSatWait);
     SetPersistentNumberNote("CM:SatCathodeSteps", nSatSteps);
     number nTime = GetCurrentTime();
     number dateFormat = 2 ; 
     number timeFormat = 2 ; 
     number format = dateFormat + 16 * timeFormat;  
     Result( FormatTimeString( nTime, format ) + "\n" );  

     Result("-- WAIT -- " + nMin + " min.  Saturating Cathode --\n");
     BringUpCathode( nSatSteps, nSatWait);
     Result("Ready\n");
     
  }

  void desaturate_cathode(object self)
  {
     number nMin;
     nDesatWait = DesatCathodeWait.DLGGetValue();
     nSatSteps = SatCathodeSteps.DLGGetValue();
     nMin = nDesatWait * nSatWait / 60;
     SetPersistentNumberNote("CM:CathDesatWait", nDesatWait);
     SetPersistentNumberNote("CM:SatCathodeSteps", nSatSteps);
     number nTime = GetCurrentTime();
     number dateFormat = 2 ; 
     number timeFormat = 2 ; 
     number format = dateFormat + 16 * timeFormat;  
     Result( FormatTimeString( nTime, format ) + "\n" );  

     Result("-- WAIT -- " + nMin + "min.  Desaturating Cathode --\n");
     BringDownCathode( nSatSteps, nDesatWait);
     Result("Ready\n");
  }
}


// Get desired defaults
number bRet

bRet = GetPersistentNumberNote("CM:CathSatSteps", nSatSteps);
if (bRet < 1)
{
      nSatSteps = 20;  // typically between 20 and 25...
      SetPersistentNumberNote("CM:CathSatSteps", nSatSteps);
}

bRet = GetPersistentNumberNote("CM:CathSatWait", nSatWait);
if (bRet < 1)
{
      nSatWait = 30; // default for saturation - 30 sec
      SetPersistentNumberNote("CM:CathSatWait", nSatWait);
}

bRet = GetPersistentNumberNote("CM:CathDesatWait", nDesatWait);
if (bRet < 1)
{
      nDesatWait = 10; // default for desat - 10 sec
      SetPersistentNumberNote("CM:CathDesatWait", nDesatWait);
}

// be sure we have a results window open...
OpenResultsWindow();

// Create Dialog
CathodeDlg     = DLGCreateDialog( "CmCathodeTool", CathodeDlgItems );


// Create items
SatCathodeStepsField  =  DLGCreateIntegerField("Steps to saturation:", SatCathodeSteps, nSatSteps, 3);
SatCathodeWaitField   =  DLGCreateIntegerField("      Up wait [sec]:", SatCathodeWait, nSatWait, 3);
DesatCathodeWaitField  = DLGCreateIntegerField("    Down wait [sec]:", DesatCathodeWait, nDesatWait, 3);
SatCathodeButton       = DLGCreatePushButton( "Saturate Cathode", "saturate_cathode");
DesatCathodeButton     = DLGCreatePushButton( "Desaturate Cathode", "desaturate_cathode");



// Add items to dialog & define the layout (2 columns, 3 rows)
CathodeDlg.DLGAddElement(SatCathodeStepsField)
CathodeDlg.DLGAddElement(SatCathodeWaitField)
CathodeDlg.DLGAddElement(DesatCathodeWaitField)

CathodeDlg.DLGAddElement(SatCathodeButton)
CathodeDlg.DLGAddElement(DesatCathodeButton)

CathodeDlg.DLGTableLayout(3,2,0)


objCathodeWindow = alloc(CMCathodeTool).Init(CathodeDlg);
objCathodeWindow.Display("CMCathodeTool")



