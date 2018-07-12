run("Blobs (25K)");
run("Radial Profile Angle", 
	"x_center=127.50 y_center=127.50 radius=127.50 starting_angle=0 integration_angle=180");
run("Clear Results"); 
for(j = 0; j < Ext.getBinSize; j++){
	setResult("Radius", j, Ext.getXValue(j)); 
	setResult("Intensity", j, Ext.getYValue(0, j)); 
}
updateResults(); 
saveAs("results", "");
