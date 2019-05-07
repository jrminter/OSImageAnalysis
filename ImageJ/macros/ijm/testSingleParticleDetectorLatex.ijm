open("C:/data/images/pol4455/Crop_Ordered POL4455.tif");
run("Median...", "radius=2");
setAutoThreshold("Default");
//run("Threshold...");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Compile and Run...", "compile=C:/Apps/ImageJ/plugins/Examples/Single_Particle_Detector.java");
run("Close");
