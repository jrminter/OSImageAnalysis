open("/Users/jrminter/dat/images/test/clumpAgX/qm-03965-KJL-027/dm3/qm-03695-KJL-027-01.dm3");
run("Enhance Contrast", "saturated=0.35");
run("Duplicate...", "title=work");
selectWindow("work");
run("8-bit");
setAutoThreshold("Default");
setOption("BlackBackground", false);
run("Convert to Mask");
run("Watershed");
// Note afterward this was 27355 in ~/Library/Preferences/IJ_Prefs.txt
run("Set Measurements...", "area mean modal min center perimeter bounding fit shape feret's redirect=qm-03695-KJL-027-01.dm3 decimal=3");
run("Analyze Particles...", "display exclude clear include add");
