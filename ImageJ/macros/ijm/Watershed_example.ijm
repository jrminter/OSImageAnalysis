// load the Blobs sample image
run("Blobs (25K)");
// invert LUT and pixel values to have dark blobs
run("Invert LUT");
run("Invert");
// run plugin on image
run("Classic Watershed", "input=blobs mask=None use min=0 max=150");
// apply LUT to facilitate result visualization
run("3-3-2 RGB");
// pre-process image with Gaussian blur
selectWindow("blobs.gif");
run("Gaussian Blur...", "sigma=3");
rename("blobs-blur.gif");
// apply plugin on pre-processed image
run("Classic Watershed", "input=blobs-blur mask=None use min=0 max=150");
// apply LUT to facilitate result visualization
run("3-3-2 RGB");