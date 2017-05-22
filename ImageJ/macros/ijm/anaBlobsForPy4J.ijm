// anaBlobsForPy4J.ijm
run("Close All");
run("Blobs (25K)");
setAutoThreshold("Default");
//run("Threshold...");
//setThreshold(126, 255);
setOption("BlackBackground", false);
run("Convert to Mask");
//run("Close");
run("Set Measurements...", "area mean modal min centroid center perimeter bounding fit shape display redirect=None decimal=3");
//run("Analyze Particles...", "exclude clear add");
//run("Close");
run("Analyze Particles...", "display exclude clear add");
