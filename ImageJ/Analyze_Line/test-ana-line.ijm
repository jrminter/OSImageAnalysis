/**********************************************************************************  
 * J. R. Minter 2013-05-07
 * Test line analysis
*********************************************************************************** */

strBasePath="C:\\Data\\atd\\images\\";
strFile="std\\line\\line.tif";
umPerPx="0.036861";

// hopefully minimal changese needed below here...
strImage=strBasePath + strFile;
strCal="channels=1 slices=1 frames=1 unit=micron pixel_width=";
strCal+=umPerPx;
strCal+=" pixel_height=";
strCal+=umPerPx;
strCal+="  voxel_depth=1.0000000 frame=[0 sec] origin=0,0";
//print(strCal);
open(strImage);
run("Properties...", strCal);
// first find the background
setAutoThreshold("Default dark");
run("Set Measurements...", "  mean center bounding redirect=None decimal=3");
run("Analyze Particles...", "size=5-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear");
// now find the line
setAutoThreshold("Default");
run("Analyze Particles...", "size=5-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display");

if(nResults==3){
  grayBkg=0.5*(getResult("Mean", 0)+getResult("Mean", 2));
  grayLin=getResult("Mean", 2);
  print("Bkg = " + grayBkg);
  print("Lin = " + grayLin);
  // for dark lines
  thrHi = 0.5*(grayBkg+grayLin);
  setThreshold(0, thrHi);
  run("Analyze Particles...", "size=5-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear");
  x=getResult("XM", 0);
  y=getResult("YM", 0);
  doWand(x, y);
  
}

