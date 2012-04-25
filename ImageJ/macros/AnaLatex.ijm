//
// AnaLatex.ijm
// Shading Correction and particle analysis of soft latex
// Open the test image "latex.tif" and then run this
//
run("Subtract Background...", "rolling=25 light sliding");
run("Median...", "radius=2");
setAutoThreshold("Otsu");
run("Convert to Mask");
run("Set Measurements...", "area centroid center perimeter shape redirect=None decimal=3");
run("Analyze Particles...", "size=1000-6000 circularity=0.80-1.00 show=[Overlay Outlines] display exclude clear include");
