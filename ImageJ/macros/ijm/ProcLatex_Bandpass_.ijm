open("/Users/jrminter/git/OSImageAnalysis/images/latex.tif");
run("Bandpass Filter...", "filter_large=40 filter_small=1 suppress=None tolerance=5 autoscale saturate");
run("Median...", "radius=3");
setAutoThreshold("Otsu");
setOption("BlackBackground", false);
run("Set Measurements...", "area perimeter fit feret's redirect=None decimal=3");
run("Analyze Particles...", "  circularity=0.80-1.00 display exclude clear include");
