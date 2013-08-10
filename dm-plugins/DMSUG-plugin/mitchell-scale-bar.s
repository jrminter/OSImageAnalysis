// Dialog to provide easy control of the scale bar on the foremost image
// The propagate tool (>>) allows the same format to be propagated to all
// open images. In the latest version of DM controlling the appearance of
// the scale bar has become moe cumbersome.
// D. R. G. Mitchell, adminnospam@dmscripting.com (remove the nospam from this email address to make it work).
// Version 1.1, October 2006
// version:20061003

// Acknowlegements to V. Hou for providing info on the componentsetcolor() / componentgetcolor() commands

// Note this script uses the function componentsetdrawingmode(number colourmode). The behaviour of this function
// changed in DM 3.10. Prior to this colourmode values of 0,1,2,3 resulted in components being B/W, B, W/B and W
// where B/W means black on white etc. In 3.10 and later colourmode values 0 and 2 turned on the background
// while 1 and 3 turned if off. To set the colour of the foreground and background, the commands
// componentsetforegroundcolor (R,G,B) and componentsetbackgroundcolor(R,G,B) are used. RGB values appear to be 0 or 1.
// This script has been tested with DM 3.9 and DM 3.11

// This function reformats the scale bars of all
// displayed images to the format of the foremost image. Spectra and uncalibrated
// images are ignored

void ReformatAllScaleBars()
{
  // Variable declaration
  number fontattribute, fontsize, textencoding, fontdrawmode, shown, i, test, inc, fred, bred, fgreen, bgreen, fblue, bblue
  imagedocument imgdoc
  image img
  imagedisplay imgdisp
  component scalebar
  string unitstring, fontface
  number xsize, ysize
  
  // Tests to see if any images are shown, if not, then it exits
  shown=CountDocumentWindowsOfType(5)
  if(shown<1) return
  
  // Get the foremost image and source the scale bar parameters from it
  image front:=getfrontimage()
  imgdisp=front.imagegetimagedisplay(0)
  test = imgdisp.ComponentCountChildrenOfType(31)
  
  // if a scale bar is present the parameters are sourced
  if(test)
  {
    scalebar=imgdisp.componentgetnthchildoftype(31,0)
    scalebar.componentgetfontinfo(fontface, fontattribute, fontsize, textencoding)
    scalebar.componentgetforegroundcolor(fred, fgreen, fblue)
    scalebar.componentgetbackgroundcolor(bred, bgreen, bblue)
    fontdrawmode=scalebar.componentgetdrawingmode()
  }
  // if a scale bar is not present on the foremost image, an alert is shown
  else
  {
    beep()
    okdialog("There is no scale bar on the foremost image!")
    exit(0)
  }

  // Loop to display all the shown images in a cascaded sequence
  // Applying the newly formatted scale bar to them
  // Uncalibrated images are ignored.

  for(i=0; i<shown; ++i)
  {
    ysize=0
    unitstring=""
    imgdoc=getimagedocument(i)
    img:=ImageDocumentGetimage(imgdoc,0)
    getsize(img, xsize, ysize)

    if (ysize>1) unitstring=getunitstring(img) // traps for 1D images

    if (unitstring!="" && ysize>1) // ingores uncalibrated images and line profiles
    {
      imgdisp = img.ImageGetImageDisplay(0)
      imgdisp.applydatabar()
      component newscalebar=imgdisp.componentgetnthchildoftype(31,0)
      newscalebar.componentsetfontinfo(fontface,fontattribute, fontsize)

      newscalebar.componentsetdrawingmode(fontdrawmode)
      newscalebar.componentsetforegroundcolor(fred, fgreen, fblue)
      newscalebar.componentsetbackgroundcolor(bred, bgreen, bblue)

    }

    imagedocumentshowatposition(imgdoc,142+inc, 24+inc)
    inc=inc+30
  }
}

// the class createbuttondialog is of the type user interface frame, and responds to interaction
// the dialog

class ScaleDialog : uiframe
{
  // sources the current dialog values and updates the scale
  // bar on the foremost image (if one is present)
  void updatefrontimage(object self)
  {
    // extracts the current settings from the dialog and sets the scale bar accordingly

    number fontsizeval, colourval, fontstringval, actualfontsize
    number fred, fgreen, fblue, bred, bgreen, bblue
    string fontface, fontsizestring

    taggroup localscalesize=self.lookupelement("sbscalesize")
    taggroup localscalefont=self.lookupelement("sbscalefont")
    taggroup localcolourlist=self.lookupelement("sbcolourlist")

    fontsizeval=localscalesize.dlggetvalue()
    colourval=localcolourlist.dlggetvalue()


    if (colourval==0 || colourval==1) // foreground colour is black, background colour (if on) is white
    {
      fred=0 // f colours are the foreground colours
      fgreen=0
      fblue=0 // ie foregound colour is black

      bred=1 // b colours are the background colours
      bgreen=1
      bblue=1 // ie backgound colour is white
    }
    
    if (colourval==2 || colourval==3)// foreground colour is white, background colour (if on) is black
    {
      fred=1 // f colours are the foreground colours
      fgreen=1
      fblue=1 // ie foregound colour is white

      bred=0 // b colours are the background colours
      bgreen=0
      bblue=0 // ie backgound colour is black
    }
    
    fontstringval=localscalefont.dlggetvalue()
    localscalefont.dlggetnthlabel(fontstringval-1,fontface)
    localscalesize.dlggetnthlabel(fontsizeval-1,fontsizestring)
    actualfontsize=val(fontsizestring)
    // checks to make sure one or more images is displayed
    number shown=CountDocumentWindowsOfType(5)
    if(shown<1)
    {
      return
    }

    // gets the foremost image and checks to see if it has a scalebar
    image front:=getfrontimage()
    imagedisplay imgdisp=front.imagegetimagedisplay(0)
    number nobar=imgdisp.componentcountchildrenoftype(31)

    if(nobar>0) // if no scale bar is present, one is added
    {
      component scalebar=imgdisp.componentgetnthchildoftype(31,0)
      scalebar.componentsetfontinfo(fontface, 0, actualfontsize)
      scalebar.componentsetdrawingmode(colourval+1)

      scalebar.componentsetforegroundcolor(fred, fgreen, fblue)
      scalebar.componentsetbackgroundcolor(bred, bgreen, bblue)

    }
  }

  void scaleonoffresponse(object self) // Responds when the "1/0" button is pressed
  {
    number shown=CountDocumentWindowsOfType(5) // number of open image windows

    if(shown<1) // trap for no open images
    {
      return
    }

    image front:=getfrontimage()
    imagedisplay imgdisp=front.imagegetimagedisplay(0)

    // determines if a scale bar (child of type 31 is present on the foremost image)
    number nobar=imgdisp.componentcountchildrenoftype(31)

    if(nobar==0) // no scale is present so add one
    {
      imgdisp.applydatabar(0)
      self.updatefrontimage()
    }
    else // scale bar is already present so remove it
    {
      component scalebar=imgdisp.componentgetnthchildoftype(31,0)
      scalebar.componentremovefromparent()
    }
  }

  void propagateresponse(object self) // response when propagate (>>) button is pressed
  {
    // trap for no open images
    number shown=CountDocumentWindowsOfType(5)

    if(shown<1)
    {
      return
    }

    // determine if the foremost image has a scalebar

    image front:=getfrontimage()
    imagedisplay imgdisp=front.imagegetimagedisplay(0)
    number nobar=imgdisp.componentcountchildrenoftype(31)

    if(nobar==0) // traps for no scale bar on the foremost image - won't propagate
    {
      return
    }

    ReformatAllScaleBars() // function to reformat all scale bars to the foremost
  }

  void scalesizechange(object self, taggroup scalesizetag)
  {
    self.updatefrontimage() // if font size is changed update foremost image
  }

  void scalefontchange(object self, taggroup scalefonttag) // if scale bar font is changed update foremost image
  {
    self.updatefrontimage()
  }

  void scalecoloursetting(object self, taggroup scalecolourtag) // if font colour is changed update foremost image
  {
    self.updatefrontimage()
  }
}

// this function creates the scale bar dialog
taggroup MakeScaleDialog()
{
  // Creates a box in the dialog which surrounds the buttons etc

  taggroup scalebox_items
  taggroup scalebox=dlgcreatebox(" Scale Bar ", scalebox_items)
  scalebox.dlgexternalpadding(3,3)
  scalebox.dlginternalpadding(5,0)

  // Creates the on/off button

  TagGroup onoffButton = DLGCreatePushButton("1/0", "scaleonoffresponse").dlginternalpadding(2,2)
  onoffbutton.dlgexternalpadding(1,2)

  // creates the propagate >> button

  TagGroup propagateButton = DLGCreatePushButton(">>", "propagateresponse").dlginternalpadding(2,2)
  propagatebutton.dlgexternalpadding(1,2)

  taggroup scalebuttongroup=dlggroupitems(onoffbutton,propagatebutton).dlgtablelayout(2,1,0).dlganchor("South")

  // Creates the scale font size pulldown menu

  TagGroup scalesize_items;
  taggroup scalesize = DLGCreatePopup(scalesize_items, 1, "scalesizechange")
  scalesize.dlgidentifier("sbscalesize")

  // edit the values in " " to change the available font sizes in your dialog

  scalesize_items.DLGAddPopupItemEntry("12");
  scalesize_items.DLGAddPopupItemEntry("18");
  scalesize_items.DLGAddPopupItemEntry("24");
  scalesize_items.DLGAddPopupItemEntry("32");
  scalesize_items.DLGAddPopupItemEntry("36");
  scalesize_items.DLGAddPopupItemEntry("48");
  scalesize_items.DLGAddPopupItemEntry("60");
  scalesize_items.DLGAddPopupItemEntry("72");

  // sets the default value of the font size menu to the 5th value (36pt)
  TagGroupSetTagAsNumber( scalesize, "Value", 5 )

  taggroup scalesizelabel=dlgcreatelabel("Font Size").dlganchor("Centre")
  taggroup scalesizegroup=dlggroupitems(scalesizelabel, scalesize)
  taggroup scaletoprow_group=dlggroupitems(scalebuttongroup,scalesizegroup).dlgtablelayout( 2,1,0)


  // Creates the scale font pulldown menu

  TagGroup scalefont_items;
  taggroup scalefonts = DLGCreatePopup(scalefont_items, 1, "scalefontchange")
  scalefonts.dlgidentifier("sbscalefont")

  // Edit the font names in " " below to change them in your dialog - Note they must match exactly the available system font names

  scalefont_items.DLGAddPopupItemEntry("Arial Narrow");
  scalefont_items.DLGAddPopupItemEntry("Courier New");
  scalefont_items.DLGAddPopupItemEntry("Microsoft Sans Serif");
  scalefont_items.DLGAddPopupItemEntry("Palatino Linotype");
  scalefont_items.DLGAddPopupItemEntry("Times New Roman");
  scalefont_items.DLGAddPopupItemEntry("Verdana");

  // sets the default value of the scale bar font menu to the 3rd value (MS Sans Serif)
  TagGroupSetTagAsNumber( scalefonts, "Value", 3 )

  taggroup scalefontlabel=dlgcreatelabel("Scale Bar Font").dlganchor("Centre")
  taggroup scalefontgroup=dlggroupitems(scalefontlabel, scalefonts)
  taggroup scalebuttonsandfont=dlggroupitems(scaletoprow_group, scalefontgroup)

  // creates a radio item for selecting the colour eg B/W = Black on White
  TagGroup colourlist_items
  taggroup colourlist = DLGCreateRadioList( colourlist_items, 0, "scalecoloursetting" )
  colourlist.dlgidentifier("sbcolourlist")
  colourlist_items.DLGAddElement( DLGCreateRadioItem( "B/W", 0 ) )
  colourlist_items.DLGAddElement( DLGCreateRadioItem( "B", 1 ) )
  colourlist_items.DLGAddElement( DLGCreateRadioItem( "W/B", 2 ) )
  colourlist_items.DLGAddElement( DLGCreateRadioItem( "W", 3 ) )
  colourlist.dlgexternalpadding(0,5)

  taggroup scalebuttons_list=dlggroupitems(scalebuttonsandfont,colourlist).dlgtablelayout(2,1,0)

  scalebox_items.dlgaddelement(scalebuttons_list)

  return scalebox
}

// This function calls the main dialog creation function, and sets up and positions the resulting dialog
void CreateDialogExample()
{
// Configure the positioning in the top right of the application window

  TagGroup scaleposition;
  scaleposition = DLGBuildPositionFromApplication()
  scaleposition.TagGroupSetTagAsTagGroup( "Width", DLGBuildAutoSize() )
  scaleposition.TagGroupSetTagAsTagGroup( "Height", DLGBuildAutoSize() )
  scaleposition.TagGroupSetTagAsTagGroup( "X", DLGBuildRelativePosition( "Inside", 1 ) )
  scaleposition.TagGroupSetTagAsTagGroup( "Y", DLGBuildRelativePosition( "Inside", 1 ) )

  TagGroup scaledialog_items;
  TagGroup scaledialog = DLGCreateDialog("Scale Dialog", scaledialog_items).dlgposition(scaleposition);
  scaledialog_items.dlgaddelement( MakeScaleDialog() );

  object dialog_frame = alloc(ScaleDialog).init(scaledialog)
  dialog_frame.display("Scale Bar");
}


// calls the above function which puts it all together

createdialogexample()