// CMSnapImageTool
// 2013-08-16 J. R. Minter
// Initial prototype
//
// Grabs an image from the CM20UT, bins as
// desired, converts to 16bit unsigned int,
// saves the stage tags to the image and
// writes to result window. Makes storing easy.


TagGroup SnapItDlg, SnapItDlgItems
Taggroup CcdSize, CcdSizeField
Taggroup Binning, BinningField
Taggroup ExpTime, ExpTimeField
Taggroup BasePath, BasePathField
Taggroup SampName, SampNameField
Taggroup ImgNum, ImgNumField 
Taggroup ResetImgNumButton, DecImgNumButton, SnapImgButton, SaveImgButton
Object   objSnapItToolWindow;

number g_nCCDsize, g_nImgNum, g_nExpTime, g_nBinning
string g_sBasePath, g_sImgName
image  g_Image

g_nCCDsize = 2048
g_nBinning = 1
g_nImgNum = 1
g_nExpTime = 0.5
g_sBasePath = "c:\\data\\atd\\images\\"
g_sImgName = "qm-03245-foo"

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

void AddStageTagsToImage (image img)
{
   TagGroup tgTest;
   String strName = GetName(img);
   Result("\n\n");
   Result(strName);
   Result("\n");   
   TagGroup tgStage = GetStageToTagGroup();
   TagGroup tgImage = ImageGetTagGroup(img);
   if(tgImage.TagGroupGetTagAsTagGroup( "Stage Coordinates", tgTest ) )
   {
      TagGroupDeleteTagWithLabel(tgImage, "Stage Coordinates" );

   }
   TagGroupAddLabeledTagGroup( tgImage, "Stage Coordinates", tgStage );
}


// This bit of code is where buttons and pulldowns generate responses.
class CmSnapImageTool : uiframe
{
  void reset_number(object self)
  {
    // get values from DLG and save
    g_nImgNum = ImgNum.DLGGetValue()
    g_nImgNum = 1
    SetPersistentNumberNote("SnapIt:nImgNum", g_nImgNum)
    ImgNum.DLGValue(g_nImgNum)
  }
  
  void decrement_number(object self)
  {
    g_nImgNum = ImgNum.DLGGetValue()
    g_nImgNum -= 1
    SetPersistentNumberNote("SnapIt:nImgNum", g_nImgNum)
    ImgNum.DLGValue(g_nImgNum)
  }
  
  void snap_image(object self)
  {
    // for now just create one
    g_nImgNum = ImgNum.DLGGetValue()
    SetPersistentNumberNote("SnapIt:nImgNum", g_nImgNum)
    ImgNum.DLGValue(g_nImgNum)
    
    g_nCCDsize = CcdSize.DLGGetValue()
    SetPersistentNumberNote("SnapIt:CCDsize", g_nCCDsize)
    CcdSize.DLGValue(g_nCCDsize)
    
    g_nBinning = Binning.DLGGetValue()
    SetPersistentNumberNote("SnapIt:Binning", g_nBinning)
    Binning.DLGValue(g_nBinning)
    
    g_nExpTime = ExpTime.DLGGetValue()
    SetPersistentNumberNote("SnapIt:ExpTime", g_nExpTime)
    ExpTime.DLGValue(g_nExpTime)
    
    g_sImgName = SampName.DlgGetStringValue()
    SetPersistentStringNote("SnapIt:ImgName", g_sImgName)
    SampName.DlgValue(g_sImgName)
    
    g_sBasePath = BasePath.DlgGetStringValue()
    SetPersistentStringNote("SnapIt:Path", g_sBasePath)
    BasePath.DlgValue(g_sBasePath)
    
    
    string name
    number size = g_nCCDsize/g_nBinning
    if (g_nImgNum < 10)
    {
      name = g_sImgName + "-0" + g_nImgNum
    }
    else
    {
      name = g_sImgName + "-" + g_nImgNum
    }
     
    g_nImgNum +=1
    SetPersistentNumberNote("SnapIt:nImgNum", g_nImgNum)
    ImgNum.DLGValue(g_nImgNum)
	
    number fMag
    number bOK = GetPersistentNumberNote("Microscope Info:Indicated Magnification", fMag)
    // result("Starting Indicated Mag: " + fMag + "\n")


    number nMag = EMGetMagnification()
    // result("Set Indicated Mag to: " + nMag + "\n")
    SetPersistentNumberNote("Microscope Info:Indicated Magnification", nMag)
    
    // TagGroup tg = self.LookUpElement("ImgNumField")
    // If (tg.TagGroupIsValid()) tg.DLGValue(g_nImgNum)
    
    image work :=  SSCGainNormalizedAcquire( g_nExpTime, 0, 0, g_nCCDsize, g_nCCDsize)
    if(g_nBinning > 1 )
    {
      Reduce(work) 
    }
    if(g_nBinning > 2 )
    {
      Reduce(work) 
    }
    
    string unitstring, imgname, imgdesc
    TagGroup tgSrcParams = ImageGetTagGroup(work)
    
    work = max(work, 0);
    work = min(work, 65535);
    number sizex, sizey, scalex, scaley
    getsize(work, sizex, sizey)
    
    image imInt := IntegerImage("Int", 2,0, sizex, sizey)
    TagGroup tgDstParams = ImageGetTagGroup(imInt)
    imInt = work
    getscale(work, scalex, scaley)
    getunitstring(work, unitstring)
    setscale(imInt, scalex, scaley)
    setunitstring(imInt, unitstring)
    taggroupcopytagsfrom(tgDstParams, tgSrcParams)
    
    DeleteImage(work)
    g_Image := imInt
    setname(g_Image, name)
    AddStageTagsToImage(g_Image)    
    ShowImage(g_Image)   
  }
  
  void save_image(object self)
  {
    g_sImgName = SampName.DlgGetStringValue()
    SetPersistentStringNote("SnapIt:ImgName", g_sImgName)
    SampName.DlgValue(g_sImgName)
    
    g_sBasePath = BasePath.DlgGetStringValue()
    SetPersistentStringNote("SnapIt:Path", g_sBasePath)
    BasePath.DlgValue(g_sBasePath)
    
    string fName = g_sBasePath + getname(g_Image) + ".dm3"
    saveImage(g_Image, fName)
     
  }
  
}

// Get desired defaults
number bRet

bRet = GetPersistentNumberNote("SnapIt:CCDsize", g_nCCDsize)
if (bRet < 1)
{
      g_nCCDsize = 2048;
      SetPersistentNumberNote("SnapIt:CCDsize", g_nCCDsize)
}

bRet = GetPersistentNumberNote("SnapIt:Binning", g_nBinning)
if (bRet < 1)
{
      g_nBinning = 1;
      SetPersistentNumberNote("SnapIt:Binning", g_nBinning)
}

bRet = GetPersistentNumberNote("SnapIt:ImgNum", g_nImgNum)
if (bRet < 1)
{
      g_nImgNum = 1;
      SetPersistentNumberNote("SnapIt:nImgNum", g_nImgNum)
}

bRet = GetPersistentNumberNote("SnapIt:ExpTime", g_nExpTime)
if (bRet < 1)
{
      g_nExpTime = 0.5;
      SetPersistentNumberNote("SnapIt:ExpTime", g_nExpTime)
}

bRet = GetPersistentStringNote("SnapIt:Path", g_sBasePath)
if (bRet < 1)
{
      g_sBasePath = "c:\\data\\";
      SetPersistentStringNote("SnapIt:Path", g_sBasePath);
}

bRet = GetPersistentStringNote("SnapIt:ImgName", g_sImgName)
if (bRet < 1)
{
      g_sImgName = "bar";
      SetPersistentStringNote("SnapIt:ImgName", g_sImgName);
}



// Create Dialog
SnapItDlg        = DLGCreateDialog(      "CmSnapImageTool", SnapItDlgItems)
// create fields
CcdSizeField     = DLGCreateIntegerField("    CCD Size: ", CcdSize, g_nCCDsize, 10)
BinningField     = DLGCreateIntegerField(" CCD Binning: ", Binning, g_nBinning, 10)
ImgNumField      = DLGCreateIntegerField(" Image Number: ", ImgNum, g_nImgNum, 10)
ExpTimeField     = DLGCreateRealField(   " Exp Time (s): ", ExpTime, g_nExpTime, 10,2)
BasePathField    = DLGCreateStringField("Base Path", BasePath, g_sBasePath, 40)
SampNameField    = DLGCreateStringField("Image Name", SampName, g_sImgName, 40)
// create buttons
ResetImgNumButton = DLGCreatePushButton( " Reset Number  ", "reset_number")
DecImgNumButton   = DLGCreatePushButton( "   (-) Number  ", "decrement_number")
SnapImgButton     = DLGCreatePushButton( "   SNAP Image  ", "snap_image")
SaveImgButton     = DLGCreatePushButton( "   SAVE Image  ", "save_image")

// Add items to dialog & define the layout (1 columns, 7 rows)
SnapItDlg.DLGAddElement(CcdSizeField)
SnapItDlg.DLGAddElement(BinningField)
SnapItDlg.DLGAddElement(ImgNumField)
SnapItDlg.DLGAddElement(ExpTimeField)
SnapItDlg.DLGAddElement(BasePathField)
SnapItDlg.DLGAddElement(SampNameField)

SnapItDlg.DLGAddElement(ResetImgNumButton)
SnapItDlg.DLGAddElement(DecImgNumButton)
SnapItDlg.DLGAddElement(SnapImgButton)
SnapItDlg.DLGAddElement(SaveImgButton)

SnapItDlg.DLGTableLayout(1,10,0);



objSnapItToolWindow = alloc( CmSnapImageTool).Init(SnapItDlg);
objSnapItToolWindow.Display("CmSnapItTool");



