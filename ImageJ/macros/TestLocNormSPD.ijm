run("Local Normalization");
selectWindow("LN of soft.tif");
run("16-bit");
run("Properties...", "channels=1 slices=1 frames=1 unit=nm pixel_width=2.02 pixel_height=2.02 voxel_depth=1 frame=[0 sec] origin=0,0");
run("Median...", "radius=2");
setAutoThreshold("Shanbhag");
// run("Close");
run("Single Particle Detector", "minarea=100 maxarea=99999 maxintrusion=4 draw=1 path=/Users/jrminter/dat/report/ report=soft.csv");
close();
