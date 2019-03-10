/* 
 * From Wayne Rasband 2018-12-14
 *
 * The latest daily build adds an Overlay.setLabelColor() function.
 * There are two versions, one that sets the label color and another
 * that sets both the label and background color. This function, and
 * other new functions, are in the macro documentation at
 *
 * http://wsr.imagej.net/developer/macro/functions.html
 *
 * Stein Rørvik <Stein.Rorvik@SINTEF.NO> wrote: 
 * 
 * I want to run Analyze Particles on a stack, but only on specific slices.
 * I want the results (which particles were analyzed or not) to be shown as an overlay.
 * If I say yes to process all slices, the results are as expected.
 * 
 * There is an individual overlay for each slice. But if I want to analyze
 * a single slice, the result overlay is "global"; that is, one overlay for
 * the entire stack. So when I process another slice, the previous result overlay
 * is lost. I think the overlay should have been applied to a single slice
 * position in this case as well.  Am I missing an option somewhere? Or is this a bug? 
 * 
 * Wayne responded:
 * It’s a bug that is fixed in the daily build (1.52j26). The following example runs
 * the particle analyzer on two slices of a stack and set the overlay color to red.
*/

run("T1 Head (2.4M, 16-bits)");
setThreshold(150, 65535);
setSlice(60);
run("Analyze Particles...", "size=400 show=Overlay slice"); 
setThreshold(250, 65535);
setSlice(62); 
run("Analyze Particles...", "size=400 show=Overlay slice");
resetThreshold;
Roi.remove;
Overlay.setStrokeColor("red");
Overlay.setStrokeWidth(1);
Overlay.setLabelFontSize(12, "bold scale");
Overlay.setLabelColor("cyan","black");
run("In [+]");