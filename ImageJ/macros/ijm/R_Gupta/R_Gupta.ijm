// R_Gupta.ijm
// 
// A script by J. R. Minter based on a question by R. Gupta
//
// Date        Who What
// ----------  ---  -----------------------------------------
// 2019-05-10  JRM  Initial prototype
//


// N.B. - change the path to fit your system
open("/Users/jrminter/Downloads/Picture1.jpg");
// We really only want the green (complementary) channel..
run("Split Channels");
selectWindow("Picture1.jpg (red)");
close();
selectWindow("Picture1.jpg (blue)");
close();
// This is our key original image
selectWindow("Picture1.jpg (green)");
//
// Make an Oval ROI just inside the boundary
makeOval(23, 11, 334, 338);
//
// We need to try some background correction. 
// There are a LOT of intensity variations & artifacts in the image... 
run("Duplicate...", "title=[for bkg]");
// Try and clean up. Better to have uniform image...
run("Unsharp Mask...", "radius=6 mask=0.8");
// None of the auto methods worked well. 
// Note to R.G.:" try a much larger dish with a white background underneath... 
setThreshold(0, 45);
setOption("BlackBackground", false);
// binarize
run("Make Binary", "thresholded remaining black");
// close the holes...
run("Close-");
// Run the watershed algorithm. 
run("Watershed");
// set up the measurements we want to make. We can always
// do post analysis based on shape classifiers...
run("Set Measurements...",
    "area mean modal min centroid center perimeter bounding fit shape display redirect=None decimal=3");
// Measure the particles
// key parameters to separate particles from artifacts:
// 1. min and max sizes
// 2. circularity. 0.5 seemed reasonable. Can vary and test effect..
run("Analyze Particles...", "size=50-2000 circularity=0.5-1.00 show=Outlines display exclude clear add");
// change the path to fit your system
saveAs("Results", "/Users/jrminter/Downloads/Results.csv");
