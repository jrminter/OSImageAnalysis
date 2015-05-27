imgDir="C:\\Data\\images\\";
imgName="magentaGrid.png";
outFile="magentaGrid.csv";

imgPath = imgDir + imgName;

open(imgPath);
run("Split Channels");
selectWindow(imgName + " (blue)");
close();
selectWindow(imgName + " (red)");
close();
selectWindow(imgName + " (green)");

run("Rotate... ", "angle=-0.37894 grid=1 interpolation=Bicubic");
makeRectangle(6, 107, 1191, 21);
run("Crop");
setAutoThreshold("Default");
//run("Threshold...");
setAutoThreshold("Moments");
run("Set Measurements...", "center redirect=None decimal=6");
run("Analyze Particles...", "clear include add");
run("Summarize");
saveAs("Results", imgDir + outFile);
run("Close");
saveAs("PNG", imgDir + "magentaGrid-det.png");
run("Close");

