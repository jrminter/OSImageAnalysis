/*
 * Making a pretty fluorogram
 * Olivier Burri, BioImaging & Optics Platform, EPFL
 */

run("Fluorescent Cells (400K)");

image = getTitle();
run("Split Channels");

channels = newArray(1,2);
thresholds = newArray(20,15);
colors = newArray("Cyan", "Magenta");
histogram_bins = 256;
histogram_max = 255;

// Run JACOP HERE
run("JACoP ", "imga=[C"+channels[0]+"-"+image+"] imgb=[C"+channels[1]+"-"+image+"] thra="+thresholds[0]+" thrb="+thresholds[1]+" pearson overlap mm cytofluo ica");

// Get the fluorogram
prettyFluorogram(image, channels, thresholds, colors, histogram_bins, histogram_max);

function prettyFluorogram(image, ch, thr, col, nbins, maxMode) {
	title=image;
	thrG = thr[0];
	thrR = thr[1];
	cG = ch[0];
	cR = ch[1];
	colG = col[cG-1];
	colR = col[cR-1];

	selectWindow("Cytofluorogram between C"+cG+"-"+title+" and C"+cR+"-"+title);
	// Get the values from the fluorogram plot.
	Plot.getValues(xpoints, ypoints);
	run("Close");
	// Get some statistics about the points
	Array.getStatistics(xpoints, xmin, xmax);
	Array.getStatistics(ypoints, ymin, ymax);

	// Which max value to use
	if (matches(maxMode, "Auto")) {
		max = xmax;
		if (xmax > ymax)
			max=ymax;
	} else {
		max = maxMode;
	}
	print("MAX:"+max);
	// Use this max to get a nice number of bins
	binWidth = (max+1)/nbins;
	//print(binWidth);
	// Build the fluorogram
	axesSize=15;
	FluorogramName = title+"Fluorogram";
	newImage(FluorogramName, "32-bit black", nbins+axesSize, nbins+axesSize, 1);

	// Populate the Thaing
	for (i=0; i<xpoints.length; i++) {
		x = round(xpoints[i]/binWidth + axesSize);
		y = round(nbins- (ypoints[i]/binWidth));
		v = getPixel(x , y);
		setPixel(x , y , v+1);
		//print(x,",",y);
	}
	getStatistics(ar, mean, min, max,sd);
	// Make pretty graph.
	newImage("xAxis", "8-bit ramp", nbins+axesSize, axesSize, 1);
	run(colG);
	getLut(redG, greenG, blueG);

	run("RGB Color");
	selectImage(FluorogramName);
	run("Add Image...", "image=xAxis x=0 y="+nbins+" opacity=100");
	//close("xAxis");
	// Make pretty graph.
	newImage("yAxis", "8-bit ramp", nbins+axesSize, axesSize, 1);
	run(colR);
	getLut(redR, greenR, blueR);

	run("RGB Color");
	run("Rotate 90 Degrees Left");
	selectImage(FluorogramName);
	run("Add Image...", "image=yAxis x=0 y=0 opacity=100");
	//close("yAxis");
	//Set LUT
	run("Fire");
	setMinAndMax(0, mean+2*sd);
	run("Log");
	setMinAndMax(0,6);

	//Axes
	setColor(255, 255, 255);
	Overlay.drawLine(axesSize, 0, axesSize, nbins+axesSize);
	Overlay.drawLine(0, nbins-1, nbins+axesSize, nbins-1);
	Overlay.add;
	// Thresholds
	setColor(redG[255], greenG[255], blueG[255]);
	Overlay.drawLine(axesSize+thrG/binWidth, 0, axesSize+thrG/binWidth, nbins-1);
	Overlay.add;
	setColor(redR[255], greenR[255], blueR[255]);
	Overlay.drawLine(axesSize, nbins-1-thrR/binWidth, nbins+axesSize, nbins-1-thrR/binWidth);
	Overlay.add;
	Overlay.show;
}