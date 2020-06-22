// Macro from Kees Straatman
// Distrobution Plotter
run("Set Measurements...", "area mean standard min limit redirect=None decimal=3");
run("Blobs (25K)");
setAutoThreshold("Default");
run("Analyze Particles...", "display");
run("Distribution Plotter", "parameter=Mean tabulate=[Number of values] automatic=[Specify manually below:] bins=50");