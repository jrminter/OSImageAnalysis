/*
PeakFinder Tool
N.Vischer, 10.11.13 23:29
http://simon.bio.uva.nl/objectj/examples/PeakFinder/peakfinder.html
(Live Overlay Profile by Jerome Mutterer)
Detects peaks along a straight line, and crates a segmented line with vertices ('handles') 
at peak positions.
A minimum spatial distance between any two peaks can be set via dMin. 
A peak can thus suppress neighbor peaks, where "Prority" is set to either amplitude or position:

"A" =highest amplitude, 
"L" =Left
"R" =Right,

Terms 'left' and 'right' refer to the position in the profile plot, 
or to a line drawn from left to right.
*/

var 
	darkBackground = true,//true if bright peaks on dark backgnd
	dMin = 0, //minimum separation distance (pixels)
	tolerance = 20, //minimum separation amplitude
	priority = "Amplitude",
	prior = "A", //choose"A". "L" or "R" (Amplitude, Left, Right)
	includeEnds = true, //endpoints are included though they are not peaks
	
	arr4x,
	arr4y,
	peakArr = newArray(0),
;


macro "PeakFinder Tool -Ce3e L0df0 C00a R3922 R7522 Rb122" {
	requires("1.48e");
	getCursorLoc(x, y, z, flags);
	xstart = x; ystart = y;
	x2=x; y2=y;   prevShift=0;    prevFlags = 0;
	overlayChanged = false;
	while (true) {
		shift = isKeyDown("shift");
		getCursorLoc(x, y, z, flags);
		if (flags & 16 == 0) 
		   exit;
		if (x!=x2 || y!=y2 || prevShift != shift || flags != prevFlags) {
			prevFlags = flags;
			prevShift = shift;
			if (xstart != x || ystart != y){
				makeLine(xstart, ystart, x, y, x, y);//polyline
				findPeaks(xstart, ystart, x, y);
				if (isKeyDown("shift")){
					getSelectionCoordinates(xx, yy);

					overlayProfile(xstart, ystart, x, y);
					overlayChanged = true;
					makeSelection("polyline", xx, yy);
				}
				else if (overlayChanged)
					Overlay.remove;
			}
		}
		x2=x; y2=y;
		wait(10);
	}
}

function findPeaks(x1, y1, x2, y2){
	dx = x2 - x1;
	dy = y2 - y1;
	sin2 = sin(atan2(dy, dx));
	cos2 = cos(atan2(dy, dx));
	profile = getProfile();
	len = profile.length;
	if (darkBackground)
		peakArr = Array.findMaxima(profile, tolerance);
	else
		peakArr = Array.findMinima(profile, tolerance);
	nMaxima = peakArr.length;
	qualifiedArr = newArray(len);
	Array.fill(qualifiedArr, 1);
	nQualified = 0;
	if (prior != "A"){
		Array.sort(peakArr);
	}
	if (prior == "R"){
		Array.invert(peakArr);
	}
	for (jj = 0; jj < nMaxima; jj++){
		pos = peakArr[jj];
		if (qualifiedArr[pos] == 1){
			nQualified ++;
			if (dMin > 1)
			for (kk = pos - (dMin -1); kk <= pos + (dMin - 1); kk++){
				if (kk >= 0 && kk < len){
					qualifiedArr[kk] = 0;
				}
			}
		}
		else
			peakArr[jj] = -1;
	}
	Array.sort(peakArr);
	Array.invert(peakArr);
	peakArr = Array.trim(peakArr, nQualified);
	if (prior != "R")
		Array.invert(peakArr);
	nVertices = nQualified + 2;//include end points for now
	arr4x = newArray(nVertices);
	arr4y = newArray(nVertices);
	for (jj = 0; jj < nQualified; jj++){
		arr4x[jj + 1] = x1 + cos2 * peakArr[jj];
		arr4y[jj + 1] = y1 + sin2 * peakArr[jj];
	}
		arr4x[0] = x1;
		arr4y[0] = y1;
		arr4x[nVertices -1] = x2;
		arr4y[nVertices -1] = y2;
	
	if (!includeEnds){//remove endpoints
		
		peakPosx = Array.slice(arr4x, 1, nVertices-2);
		peakPosy = Array.slice(arr4y, 1, nVertices-2);
	}
	if (includeEnds)//remove endpoints
		makeSelection("polyline", arr4x, arr4y);
	else
		makeSelection("polyline", peakPosx, peakPosy);

	showStatus("nPeaks= " + nQualified);
}



macro "Insert Peak [1]"{
	if (!startsWith(getInfo("command.name"), "^"))
		exit("Locate cursor and call command via shortcut '1'");
	getCursorLoc(mousex, mousey, z, flags);

	getSelectionCoordinates(xx, yy);
	len = xx.length ;
	dx1 = xx[len - 1] - xx[0];
	dy1 = yy[len - 1] - yy[0];
	phi1 = atan2(dy1, dx1);

	dx2 = mousex - xx[len - 1];
	dy2 = mousey - yy[len - 1];
	phi2 = atan2(dy2, dx2);

	rad = sqrt(dx2 * dx2 + dy2 * dy2) * cos(phi1 - phi2);
	dx3 = cos(phi1) * rad;
	dy3 = sin(phi1) * rad;

	xInsert = xx[len - 1] + dx3;
	yInsert = yy[len - 1] + dy3;
	if (xInsert < 0 || xInsert >= getWidth || yInsert < 0 || yInsert >= getHeight)
		exit;
	found = 0;
	for (jj = 0; jj < len; jj++){
		a = xInsert - xx[jj];
		b=0;
		if (jj < len - 1)
			b = xInsert - xx[jj + 1];
			
		c = yInsert - yy[jj];
		d=0;
		if (jj < len - 1) 
			d = yInsert - yy[jj + 1];
		 
		if (a * b < 0 || c * d < 0)
			found = jj + 1;
	}
	if (found == 0){
		if (abs (xInsert - xx[0]) > abs (xInsert - xx[len-1]) || abs (yInsert - yy[0]) > abs (yInsert - yy[len-1]))
			found = len;
	}
	len++;
	xx2 = newArray(len);
	yy2 = newArray(len);
	kk = 0;
	for (jj = 0; jj < len; jj++){
		if (jj == found){
			xx2[jj] = xInsert;
			yy2[jj] = yInsert;
		}
		else{
			xx2[jj] = xx[kk];
			yy2[jj] = yy[kk];
			kk++;
			
		}
			
	}
	makeSelection("polyline", xx2, yy2);

}


macro "Kill Peak [2]"{
	if (!startsWith(getInfo("command.name"), "^"))
		exit("Locate cursor and call command via shortcut '2'");
	getCursorLoc(x, y, z, flags);
	if(selectionType == 6){
		getSelectionCoordinates(xx1, yy1);
		len = xx1.length;
		if (len == 2)
			return;
		minRad = 1e6;
		for (jj = 0; jj <len; jj++){
			dx = x - xx1[jj];
			dy = y - yy1[jj];
			dd = sqrt(dx * dx + dy * dy);
			if (dd < minRad){
				minRad = dd;
				jjMin = jj;
			}
		}
		if (minRad >= 10 /getZoom)
			showStatus("No Vertex found");
		else{
			xx2 = newArray(len-1);
			yy2 = newArray(len-1);
			kk = 0;
			for (jj = 0; jj <len; jj++){
				if (jj != jjMin){
					xx2[kk] = xx1[jj];	
					yy2[kk++] = yy1[jj];	
				}
			}
			makeSelection("polyline", xx2, yy2);
		}
	}
}


macro "Find Peaks [3]"{
	if (selectionType != 5 && selectionType != 6)
		exit("Line or segmented line expected");
	getSelectionCoordinates(xx, yy);
	findPeaks(xx[0], yy[0], xx[xx.length-1], yy[yy.length-1]);
}


macro "Show Marked Profile [4]"{
	if (selectionType !=6) exit;
	close("Found Peaks*");
	getSelectionCoordinates(xx, yy);

	profile =getProfile;
	makeSelection("polyline", xx, yy);

	prLen = profile.length;
	nVertices = xx.length;
	Plot.create("Found Peaks", "D [pixel]", "Y", profile);
	//Plot.setFrameSize(300, 150);
	Plot.show;
	run("RGB Color");
	dotsX = newArray(nVertices);
	dotsY = newArray(nVertices);
	DeltaD = newArray(nVertices);
	for (jj= 0; jj < nVertices; jj++){
		plotX = round(sqrt(pow(xx[jj] - xx[0], 2) + pow(yy[jj] - yy[0], 2)));
		plotX = maxOf(0, plotX);
		plotX = minOf(prLen-1, plotX);
		plotY = profile[plotX];
		dotsX[jj] = plotX;
		dotsY[jj] = plotY;
		if (jj > 0)
			DeltaD[jj] = dotsX[jj] - dotsX[jj - 1];
	}
	Distance = dotsX; Value = dotsY;
	Array.show("Peak Values(row numbers)", Distance, Value, DeltaD);
	for (jj= 0; jj <nVertices; jj++){
		if (includeEnds && (jj == 0) || (jj == nVertices - 1))
			continue;
		x= dotsX[jj];
		y = dotsY[jj];
		toUnscaled(x, y);
		makeOval(x-4, y-4 + 1, 8, 8);
		changeValues(0x0ffffff, 0x0ffffff, 0x0ff00ff);	
	}
	
	xval = newArray(0, dMin); //unscale trick
	yval = newArray(0, tolerance);
	toUnscaled(xval, yval);
	ww = abs(xval[0] - xval[1]);
	hh = abs(yval[0] - yval[1]);
	
	setFont("Monospaced", 12, "antiliased");
	setForegroundColor(0x0aa00);
	fillRect(6, getHeight-hh-4,  4, hh);
	drawString("Tolerance="+ tolerance, 25, getHeight-2);
	if (dMin > 1){
		setForegroundColor(0x0aa0000);
		fillRect(getWidth - ww - 2, getHeight-18,  ww, 4);
		drawString( "Priority='" + prior + "'  dMin=" + dMin, getWidth - 160, getHeight -2);	
	}
	run ("Select None");
}


//author: Jerome Mutterer
function overlayProfile(xa,ya,xb,yb) {
	Overlay.remove;
	p = getProfile();
	Array.getStatistics(p, min, max, mean, stdDev);
	List.setMeasurements;
	text = 'Length:'+d2s(List.getValue('Length'),2)+'\nmin:'+d2s(min,2)+'\nmax:'+d2s(max,2);
	setFont('SanSerif', 14, 'bold antialiased');
	setColor('black');
	Overlay.drawString(text, 10-1, 20-1);
	setColor('cyan');
	Overlay.drawString(text, 10, 20);
	setColor('green');	
	setLineWidth(2);
	for (i=0;i<p.length;i++) {
		xs = (xb-xa)/p.length;
		ys = (ya-yb)/p.length;
		d = 100-100*p[i]/max;
		a = atan ((yb-ya)/(xb-xa));
		x = xa+i*xs-d*sin(a);
		y = ya-i*ys+d*cos(a);
		if (i==0)
			Overlay.moveTo(x, y); 
		else
			Overlay.lineTo(x, y); 
	}
	Overlay.show;

}

macro "Settings...[5]"{
	url = "http://simon.bio.uva.nl/objectj/examples/PeakFinder/peakfinder.html";
	Dialog.create("Settings");
	Dialog.addCheckbox("Dark Background", darkBackground);
	Dialog.addNumber("Tolerance:", tolerance);
	Dialog.addNumber("Min distance:", dMin);
	Dialog.addChoice("Priority:", newArray("Amplitude", "Left Position", "Right Position"), priority);
	Dialog.addHelp(url);
	Dialog.show();
	darkBackground =  Dialog.getCheckbox();
	tolerance = Dialog.getNumber();
	dMin = Dialog.getNumber();;
	priority = Dialog.getChoice();
	prior = substring(priority, 0, 1);
  
}