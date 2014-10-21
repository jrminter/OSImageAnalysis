// This macro white balances RGB to a selected region (equal R,G,B =gray)
//    draw a region prior to running the macro
// Vytas Bindokas; Oct 2006, Univ. of Chicago
//

ti=getTitle;
run("Set Measurements...", "  mean redirect=None decimal=3");
roiManager("add");
                if (roiManager("count")==0)
               exit("you must draw region first");
roiManager("deselect");
run("RGB Stack");
roiManager("select",0);
setSlice(1);
run("Measure");
R=getResult("Mean");
setSlice(2);
run("Measure");
G=getResult("Mean");
setSlice(3);
run("Measure");
B=getResult("Mean");
print(B);
roiManager("reset");
run("Select None");
run("16-bit");
run("32-bit");
t=((R+G+B)/3);

setSlice(1);
dR=R-t;
if (dR<0){
run("Add...", "slice value="+abs(dR));
} else if (dR>0) {
run("Subtract...", "slice value="+abs(dR));
}

setSlice(2);
dG=G-t;
if (dG<0){
run("Add...", "slice value="+abs(dG));
} else if (dG>0) {
run("Subtract...", "slice value="+abs(dG));
}
setSlice(3);
dB=B-t;
if (dB<0){
run("Add...", "slice value="+abs(dB));
} else if (dB>0) {
run("Subtract...", "slice value="+abs(dB));
}
run("16-bit");
run("Convert Stack to RGB");
selectWindow("ROI Manager");
run("Close");
selectWindow("Results");
run("Close");
selectWindow("Log");
run("Close");
//selectImage(1);
//run("Convert Stack to RGB");
//rename("original");
selectWindow(ti);
close();
print(dR);
print(dG);
print(dB);

