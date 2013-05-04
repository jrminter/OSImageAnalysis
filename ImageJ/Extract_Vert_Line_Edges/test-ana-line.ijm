/**********************************************************************************  
 * J. R. Minter Wed Apr 17 23:11:07 EDT 2013
 * N.B. the bottom of this image looks out of focus, even though I adjusted the stage.
 * check it out in analySIS tomorrow...
 * 
 * Idea: just use the center of the CCD and collect more images and average.
 * This assumes dark lines on a light background - i.e. transmission measurements on the BX-61
 * The plan:
 * 1. use the background detection to get the mean gray level for each side along
 *    with the bounding box and COG of each ROI
 * 2. Use the deltaGray to compute the specified boundaries to compute line width
 *    (0.50) and sharpness (0.25, 0.75) from exported line points. Use the regression
 *    residuals to compute raggedness,
 * 3. Will need to move this into a plugin for optimum performance 
*********************************************************************************** */

open("C:\\Users\\jrminter\\Documents\\work\\proj\\QM13-08A-Shevlin\\dat\\ek\\chrome-line\\bx61-raw-tif\\refl-obj-chrome-line-v.tif");
run("Properties...", "channels=1 slices=1 frames=1 unit=pixel pixel_width=1 pixel_height=1 voxel_depth=1 frame=[0 sec] origin=0,0");
// first find the background
setAutoThreshold("Default dark");
run("Set Measurements...", "  mean center bounding redirect=None decimal=3");
run("Analyze Particles...", "size=500-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear");
// now find the line
setAutoThreshold("Default");
run("Analyze Particles...", "size=500-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display");




