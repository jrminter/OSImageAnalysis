run("32-bit");
run("Level Local Norm", "sigma1=6 sigma2=20");
run("16-bit");
run("Median...", "radius=2");
setAutoThreshold("Shanbhag");
run("Single Particle Detector", "minarea=100 maxarea=99999 maxintrusion=4 draw=1 path=/Users/jrminter/dat/report/ report=soft.csv");
