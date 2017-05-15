// This macros let the user save all open image and text windows in a so called workspace folder
// and restore them all at once with the 'restore workspace' macro
// a 'workspaces' directory must exist and be set up using the 'workspaces settings' macro
// author jerome.mutterer@ibmp-ulp.u-strasbg.fr

macro "Workspaces settings" {
// declares a workspaces directory
wsdir = getDirectory(" Select or create a Workspaces directory");
call("ij.Prefs.set", "workspaces.path", wsdir);
}

macro "Save Workspace [F1]" {
line="";
// checks whether a workspaces directory has been declared
path = call("ij.Prefs.get",  "workspaces.path", "nopath");
if (path=="nopath") exit ("No 'workspaces' directory set up");

// Creates the save workspace dialog 
Dialog.create("Save Workspace ");
  Dialog.addString ("name",tstamp()+".ijw",20);
  Dialog.addCheckbox ("Close All windows", true);
Dialog.show();
wsName =  Dialog.getString();
caw= Dialog.getCheckbox();
if (!endsWith(wsName,".ijw")) wsName=wsName+".ijw";
wsPath = path+wsName;
if (File.exists(wsPath)) exit("This workspace exists !\nChoose another name or \nDelete existing folder.");
File.makeDirectory(wsPath);

// start with saving non image windows.
list = getList("window.titles");
if (list.length>0) for (i=0; i<list.length; i++) {
  selectWindow(list[i]);
  if (list[i]=="Results") { 
    run("Text...", "save=["+wsPath+File.separator+"ws_results.xls]");
    line = ""+line+"text;ws_results.xls;Results"+"\n"; }
else if (list[i]=="Log") {
  run("Text...", "save=["+wsPath+File.separator+"log.txt]");
  line = ""+line+"text;log.txt;Log"+"\n"; }
else if (list[i]=="ROI Manager") {
  roiManager("Save", wsPath+File.separator+"ws_roimanager.zip");
  line = ""+line+"text;ws_roimanager.zip;ROI Manager"+"\n"; }
else { // we have another type of text window, (eg macro), we can try to save it
  contents = getInfo("window.contents");
  name = list[i];
  while (File.exists(wsPath+File.separator+name)) { name="_"+name; }
  f=File.open(wsPath+File.separator+name);
  print (f,contents);
  c=File.close(f); 
  line = ""+line+"text;"+name+";"+list[i]+"\n"; }
if (caw) run ("Close");
}

// then save all image windows as tif.
ids=getIDs();
for (i=0;i<ids.length;i++){
selectImage(ids[i]);
title=getTitle();
getDimensions(width, height, channels, slices, frames);
getCursorLoc(x, y, z, modifiers);
getLocationAndSize(xw, yw, wwidth, wheight);
line = ""+line+ids[i]+";"+title+";"+channels+";"+slices+";"+frames+";"+z+";"+xw+";"+yw+";"+wwidth+";"+wheight+"\n";
// save as tif as in saveAs("Tiff", "C:\\Documents and Settings\\mutterer\\Bureau\\embryos.tif");
saveAs("Tiff", wsPath+File.separator+ids[i]+".tif");
rename(title);
if (caw) run ("Close");
}

// finally create
f=File.open(wsPath+File.separator+"content.ijw");
print (f,line);
c=File.close(f); 
showStatus ("Workspace saved");
}

macro "Restore Workspace [F2]" {
// checks whether a workspaces directory has been declared
path = call("ij.Prefs.get",  "workspaces.path", "nopath");
if (path=="nopath") exit ("No 'workspaces' directory found");
// Creates the save workspace dialog 
Dialog.create("Restore Workspace ");
  ews = getEWS(path);
  if (ews.length>0) Dialog.addChoice ("existing WS",ews);
  else Dialog.addMessage("- no existing workspace");
Dialog.show();
path = path+Dialog.getChoice();
// get the contents.iws file and process it.
str = File.openAsString(path+File.separator+"content.ijw");
lines=split(str,"\n");
for (i=0;i<lines.length;i++) {
e = split (lines[i],";");
if (e[0]=="text") { //restore text window
if (e[1]=="ws_roimanager.zip") { roiManager("Open", path+e[1] ); }
else if (e[1]=="ws_results.xls") { run("Results...", "openasstring...=["+path+e[1]+"]"); }
else if (e[1]=="log.txt") { 
str = File.openAsString(path+File.separator+"log.txt");
print(str);
}
else { run("Edit...", "open=["+path+e[1]+"]"); }
} else if (e[0]<0) { //restore image
open (path+File.separator+e[0]+".tif");
rename (e[1]);
setLocation (e[6],e[7],e[8],e[9]);
if (e[5]>1) setSlice (e[5]);
} 
}
}

// functions below

function getIDs() {
a = newArray(nImages); for (i=1;i<=nImages;i++) {selectImage(i);a[i-1]=getImageID();}
return a;
}

function getEWS(path) {
count=0; list=getFileList(path); wslist=list;
for (i=0;i<list.length;i++){ if (endsWith(list[i],".ijw/")) { wslist[count]=list[i]; count++; } }
shortlist = newArray(count); 
for (i=0;i<count;i++){ shortlist[i]=wslist[i];}
return shortlist ;
}

function tstamp(){  
getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);   
month++; if (month<10) month="0"+month;
if (dayOfMonth<10) dayOfMonth="0"+dayOfMonth;
if (hour<10) hour="0"+hour;
if (minute<10) minute="0"+minute;
if (month<10) second="0"+second;
s=""+year+""+month+""+dayOfMonth+""+hour+""+minute+""+second;
return s;
}
