/*
 * Goal: Measure Volume of bubbles on a 2D image
 * Romain Guiet romain.guiet@epfl.ch 2015-10-09
 *
 * Strategy: Measure area of each bubble, approximate a radius and calculate a volume
 *
 * IP Strategy:
 * - get seed points, using find maxima on a blured image
 * - detect bubbles boundaries, using Level sets with the previously detected seed points
 * - analyze particles to keep only the roundish objects
 * - from the area, calculate the radius and volume and populate back the result table
 */


// start of the macro
closeImages  = false;
roiManager("Reset");
run("Clear Results");

// set the measurements
run("Set Measurements...", "area limit display redirect=None decimal=3");  // area, limited to threshold, display label

title = getTitle(); // get the title of the original image to select it later

// detect the center of the bubbles
run("Duplicate...", "title=gb2");
run("Gaussian Blur...", "sigma=2"); // apply a gaussian blur
run("Find Maxima...", "noise=10 output=[Point Selection] light");
// and look for local maxima to retrieve the center, use as seed points at the next step
// detect bubbles boundaries
selectImage(title);
run("Duplicate...", "title=med2");
run("Median...", "radius=2");  // denoise a bit before using level sets
/*
* Restore the (previously detected) seed points on this image and use
* level sets (you can try different parameters)
*/
run("Restore Selection");
run("Level Sets", "method=[Active Contours] use_fast_marching grey_value_threshold=40 distance_threshold=0.30 advection=2.20 propagation=1 curvature=1 grayscale=50 convergence=0.0050 region=outside");
selectImage("Segmentation of med2");

// invert the image (for the analyze particles step)
run("Invert");

// rename the image so the rows in result table mention the current image analyzed
rename(title+"-mask");

// detect roundish particles, calculate radius ...
selectImage(title+"-mask");

// you can change circularity parameters
run("Analyze Particles...", "size=5-Infinity circularity=0.80-1.00 display add"); 

Vtotal = 0 ;
resultNbr = nResults;
for ( rowIndex = 0 ; rowIndex < resultNbr ; rowIndex++){
    area = getResult("Area", rowIndex);
    radius = sqrt( area / PI) ;
    Volume = 4 * PI * pow(radius,3) / 3 ;
    setResult("radius",rowIndex,radius);
    setResult("Volume",rowIndex,Volume);
    Vtotal = Vtotal + Volume;
}

// print the total volume
print("Vtotal : "+title+" = "+Vtotal);

// prepare an ouput image
selectImage(title);
roiManager("Show All without labels");
run("Flatten");
rename(title+"-results");

if (closeImages){
    // close unnecessary images
    selectImage("gb2");
    close();
    selectImage("med2");
    close();
    selectImage(title+"-mask");
    close();
}
