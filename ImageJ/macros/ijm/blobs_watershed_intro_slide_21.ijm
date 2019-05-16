/*  blobs_watershed_intro_slide_21.ijm
 *  
 *  A Fiji macro constructed from
 *  http://imagej.github.io/presentations/2017-05/fiji-introduction/#/21
 *  
 *     Date     Who  What
 *  ----------  ---  --------------------------------------------------
 *  2019-05-16  JRM  macro constructed using the macro recorder while
 *                   working through the instructions
 * 
*/

run("Close All");
run("Blobs (25K)");
run("Duplicate...", " ");
run("Auto Threshold", "method=Default white");
setOption("BlackBackground", true);
run("Dilate");
run("Dilate");
run("Make Binary");
run("Convert to Mask");
run("Watershed");
run("Analyze Particles...", "exclude clear add");