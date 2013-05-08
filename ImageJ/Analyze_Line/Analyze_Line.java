import ij.*;
import ij.plugin.*;
import ij.plugin.filter.*;
import ij.plugin.Animator.*;
import ij.process.*;
import ij.gui.*;
import ij.gui.GenericDialog;
import ij.measure.*;
import ij.text.*;
import java.util.*;
import java.awt.*;
import java.awt.event.*;
import ij.plugin.*;
import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;
import ij.Prefs;

/*
* ImageJ plug-in Analyze_Line.java
* 
* Copyright 2013 by John Minter, released under GPL
* You may use this as you see fit. Please cite and send updates and
* suggestions to benefit all of us. A rising tide lifts all ships...
* 
* This is a plug-in filter designed to measure line segments and
* output results for analysis in R. This assumes a calibrated
* line segment. 
* 
* Created by John Minter 2013-05-08
* Revision History
*    Date       Version    Comments
* 2013-05-08   0.1.100     Initial prototype. 

*  TO DO:
*  1. 
*    
*/

public class Analyze_Line implements PlugInFilter {
	/** Display results in the ImageJ console. */
	public static final int SHOW_RESULTS = 1;
	public static final int SHOW_OUTLINES = 4;
	public static final int EXCLUDE_EDGE_PARTICLES = 8;
	public static final int SHOW_SIZE_DISTRIBUTION = 16;
	public static final int SHOW_PROGRESS = 32;
	public static final int CLEAR_WORKSHEET = 64;
	public static final int RECORD_STARTS = 128;
	public static final int DISPLAY_SUMMARY = 256;
	public static final int SHOW_NONE = 512;
	// public static final int FLOOD_FILL=1024;
	public static final int SHOW_MASKS = 4096;
	
	protected static final int NOTHING = 0;
	protected static final int OUTLINES = 1;
	protected static final int MASKS = 2;
	protected static final int ELLIPSES = 3;
	protected static final int INCLUDE_HOLES = 1024;
	
	private double m_dMinSize = 5., m_dMaxSize=9999999.;

	private ResultsTable m_rt = new ResultsTable();
	private ImagePlus m_imp;
	private boolean  m_bDraw; // draw into the overlay
	private int m_nWidth;
	private int m_nHeight;
	
	private String strVersion = "Analyze Line v0.1.100";
	
	public int setup(String arg, ImagePlus imp) {
		// Ask to process stacks.
		// SNAPSHOT: We always need a snapshot, also if not needed for
		// undo (e.g. in case of a stack).
		m_imp=imp;
		return IJ.setupDialog(imp, DOES_8G | DOES_16 | SNAPSHOT);
	}


	public void run(ImageProcessor ip) {
		if (IJ.versionLessThan("1.46i"))
			return;
		// 1 - Ask for parameters:
		double dMaxIntPx = 4.0d;
		String strPrefsDir = Prefs.getPrefsDir();
		String strReportDir = Prefs.getString(".rptPath.pth");
		if(strReportDir==null) strReportDir="replace";
		String strReportFile = Prefs.getString(".rptFile.fil");
		if(strReportFile==null) strReportFile="me";
		
		String strMinAreaPx = Prefs.getString(".minArea.px");
		if(strMinAreaPx==null) strMinAreaPx="10.0";
		double dMinAreaPx = Double.valueOf(strMinAreaPx);
		
		String strMaxAreaPx = Prefs.getString(".maxArea.px");
		if(strMaxAreaPx==null) strMaxAreaPx="999999.0";
		double dMaxAreaPx = Double.valueOf(strMaxAreaPx);

		String strGapPx = Prefs.getString(".gap.px");
		if(strGapPx==null) strGapPx="5.0";
	  double dGapPx = Double.valueOf(strGapPx);

		String strLoThrFr = Prefs.getString(".loThr.fr");
		if(strLoThrFr==null) strLoThrFr="0.25";
		double dLoThrFr = Double.valueOf(strLoThrFr);

	  String strMedThrFr = Prefs.getString(".medThr.fr");
		if(strMedThrFr==null) strMedThrFr="0.50";
		double dMedThrFr = Double.valueOf(strMedThrFr);

	  String strHiThrFr = Prefs.getString(".hiThr.fr");
		if(strHiThrFr==null) strHiThrFr="0.75";
		double dHiThrFr = Double.valueOf(strHiThrFr);
		
		
		String strDraw = Prefs.getString(".draw.Line");
		if(strDraw==null) strDraw="1.0";
		double dDraw = Double.valueOf(strDraw);
		
		// Do the dialog box
		GenericDialog gd = new GenericDialog(strVersion);
		gd.addNumericField("   minArea  [sq px]:", dMinAreaPx, 1);
		gd.addNumericField("   maxArea  [sq px]:", dMaxAreaPx, 1);
		gd.addNumericField("   gap        [px] :", dGapPx, 1);
		gd.addNumericField("Lo  Threshold [fr] :", dLoThrFr, 2);
		gd.addNumericField("Med Threshold [fr] :", dMedThrFr, 2);
		gd.addNumericField("Hi  Threshold [fr] :", dHiThrFr, 2);
		gd.addNumericField(" draw into overlay:", dDraw, 1);
		gd.addStringField ("              path:", strReportDir);
		gd.addStringField ("            report:", strReportFile);
		gd.showDialog();
		if (gd.wasCanceled()) return;
    
    // 2 - Retrieve parameters from the dialog     
    dMinAreaPx = gd.getNextNumber();
    dMaxAreaPx = gd.getNextNumber();
    dGapPx = gd.getNextNumber();
    dLoThrFr = gd.getNextNumber();
    dMedThrFr = gd.getNextNumber();
    dHiThrFr = gd.getNextNumber();
    dDraw = gd.getNextNumber();
    strReportDir = gd.getNextString();
    strReportFile = gd.getNextString();
        
    m_bDraw = true;
    if(dDraw < 1.0 ) m_bDraw = false;
        
    strMinAreaPx = String.format("%.1f", dMinAreaPx );
    strMaxAreaPx = String.format("%.1f", dMaxAreaPx );
    strGapPx     = String.format("%.1f", dGapPx );
    strLoThrFr   = String.format("%.2f", dLoThrFr );
    strMedThrFr  = String.format("%.2f", dMedThrFr );
    strHiThrFr   = String.format("%.2f", dHiThrFr );

    strDraw = String.format("%.1f", dDraw );

    String strReportPath = strReportDir + strReportFile;
    Prefs.set("minArea.px", strMinAreaPx);
		Prefs.set("maxArea.px", strMaxAreaPx);
		Prefs.set("gap.px", strGapPx);
		Prefs.set("loThr.fr", strLoThrFr);
		Prefs.set("medThr.fr", strMedThrFr);
		Prefs.set("hiThr.fr", strHiThrFr);
		Prefs.set("draw.Line", strDraw);   
    Prefs.set("rptPath.pth", strReportDir);
		Prefs.set("rptFile.fil", strReportFile);

		Prefs.savePreferences();

		// 3. First some house-keeping...	
		m_nWidth = ip.getWidth();
	  m_nHeight = ip.getHeight();

		if (m_imp.isInvertedLut()) {
			IJ.run("Invert");
			IJ.run("Invert LUT");
		}
		String iName = m_imp.getTitle();
		IJ.run("Colors...",
				"foreground=white background=white selection=yellow");
		Calibration cal = m_imp.getCalibration();
		float ps = (float) cal.pixelWidth;
		int measurements = Analyzer.getMeasurements(); // defined in Set Measurements dialog
		Analyzer.setMeasurements(0);
		
		// make sure at least area, cennter of mass, and rect are measured		
		measurements = Analyzer.AREA + 
				Analyzer.CENTER_OF_MASS + 
				Analyzer.MEAN + 
				Analyzer.RECT;
		int options = 0;

		// 4. Now measure background ROIS intensities on a duplicate
		ImagePlus tImp = m_imp.duplicate();
		ImageProcessor tIp = tImp.getProcessor();
		IJ.setAutoThreshold(tImp, "Default dark");

		Analyzer.setMeasurements(measurements);
		ParticleAnalyzer pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(tImp, tIp);
		double dGrayMuL = m_rt.getValue("Mean", 0);
		double dGrayMuR = m_rt.getValue("Mean", 1);
		double dGrayMuBkg = (dGrayMuL + dGrayMuR)/2.0;
		IJ.log("mean gray bkg " + dGrayMuBkg);
		m_rt.deleteRow(0);
		m_rt.deleteRow(0);
		tImp.close();

		// 5. Now measure line ROI intensity on a duplicate
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		IJ.setAutoThreshold(tImp, "Default");
		pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(tImp, tIp);
		double dGrayMuLine = m_rt.getValue("Mean", 0);
		IJ.log("mean gray line " + dGrayMuLine);
		m_rt.deleteRow(0);
		tImp.close();

		double dDeltaGray = dGrayMuBkg - dGrayMuLine;

		// 6. Compute the threshold for low delta fraction

		double dThr = dGrayMuLine + dLoThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		tIp.setThreshold(0, dThr,  ImageProcessor.NO_LUT_UPDATE);
		tImp.updateImage();
		pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(tImp, tIp);
		// get the centroids in microns and convert to px
		float fX = (float) m_rt.getValue("XM", 0);
		fX /= ps;
		float fY = (float) m_rt.getValue("YM", 0);
		fY /= ps;
		int iX = (int) fX;
		int iY = (int) fY;
		tImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		Roi lineRoi = tImp.getRoi();
		int nPts = lineRoi.getConvexHull().npoints;
		int iXpts[] = lineRoi.getConvexHull().xpoints;
		int iYpts[] = lineRoi.getConvexHull().ypoints;
		float xPts[] = new float[nPts];
		float yPts[] = new float[nPts];
		for (int k=0; k < nPts; k++) {
			xPts[k] = (float) iXpts[k];
			yPts[k] = (float) iYpts[k];		
		}
				
	  FloatPolygon linePolyHull = new FloatPolygon(xPts, yPts, nPts);
	  PolygonRoi hullRoi = new PolygonRoi(linePolyHull, Roi.POLYGON);
		hullRoi.setStrokeColor(Color.yellow);

		linePolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
		PolygonRoi interpolatedHullRoi= new PolygonRoi(linePolyHull.duplicate(), Roi.POLYGON);
		interpolatedHullRoi.setStrokeColor(Color.blue);
		
		int nHullPolyPts=linePolyHull.npoints;
		double xh[] = new double[nHullPolyPts];
		double yh[] = new double[nHullPolyPts];
		double loxr[] = new double[nHullPolyPts];
		double loyr[] = new double[nHullPolyPts];
		double loxl[] = new double[nHullPolyPts];
		double loyl[] = new double[nHullPolyPts];
		for (int i=0; i<nHullPolyPts; i++){
			loxr[i]=-9999999.0;
			loyr[i]=-9999999.0;
			loxl[i]=-9999999.0;
			loyl[i]=-9999999.0;
		}
		
		int nLoPtsL = 0;
		int nLoPtsR = 0;
		double dXt, dYt;
		
		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- dGapPx)){
        	//keep - sep from bottom
        	dXt = (xh[i] - fX)*ps;
        	dYt = (yh[i] - fY)*ps;
        	if(dXt > 0){
        		// it is a right side
        		loxr[nLoPtsR]=dXt;
        		loyr[nLoPtsR]=dYt;
        		nLoPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		loxl[nLoPtsL]=dXt;
        		loyl[nLoPtsL]=dYt;
        		nLoPtsL += 1;		
        	}
        }
			}
		}
		tImp.close();
		
		// 7. Compute the threshold for hi delta fraction

	  dThr = dGrayMuLine + dHiThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		tIp.setThreshold(0, dThr,  ImageProcessor.NO_LUT_UPDATE);
		tImp.updateImage();
		pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(tImp, tIp);
		// get the centroids in microns and convert to px
		fX = (float) m_rt.getValue("XM", 0);
		fX /= ps;
		fY = (float) m_rt.getValue("YM", 0);
		fY /= ps;
		iX = (int) fX;
		iY = (int) fY;
		tImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		lineRoi = tImp.getRoi();
		nPts = lineRoi.getConvexHull().npoints;
		iXpts = lineRoi.getConvexHull().xpoints;
		iYpts = lineRoi.getConvexHull().ypoints;
		xPts = new float[nPts];
		yPts = new float[nPts];
		for (int k=0; k < nPts; k++) {
			xPts[k] = (float) iXpts[k];
			yPts[k] = (float) iYpts[k];		
		}
				
	  linePolyHull = new FloatPolygon(xPts, yPts, nPts);
	  hullRoi = new PolygonRoi(linePolyHull, Roi.POLYGON);
		hullRoi.setStrokeColor(Color.yellow);

		linePolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
		interpolatedHullRoi= new PolygonRoi(linePolyHull.duplicate(), Roi.POLYGON);
		interpolatedHullRoi.setStrokeColor(Color.blue);
		
		nHullPolyPts=linePolyHull.npoints;
		xh = new double[nHullPolyPts];
	  yh = new double[nHullPolyPts];
		double hixr[] = new double[nHullPolyPts];
		double hiyr[] = new double[nHullPolyPts];
		double hixl[] = new double[nHullPolyPts];
		double hiyl[] = new double[nHullPolyPts];
		for (int i=0; i<nHullPolyPts; i++){
			hixr[i]=-9999999.0;
			hiyr[i]=-9999999.0;
			hixl[i]=-9999999.0;
			hiyl[i]=-9999999.0;
		}
		
		int nHiPtsR = 0;
		int nHiPtsL = 0;
		
		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- dGapPx)){
        	//keep - sep from bottom
        	dXt = (xh[i] - fX)*ps;
        	dYt = (yh[i] - fY)*ps;
        	if(dXt > 0){
        		// it is a right side
        		hixr[nHiPtsR]=dXt;
        		hiyr[nHiPtsR]=dYt;
        		nHiPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		hixl[nHiPtsL]=dXt;
        		hiyl[nHiPtsL]=dYt;
        		nHiPtsL += 1;		
        	}
        }
			}
		}
		tImp.close();

		// 8. Compute the threshold for the medium delta fraction

		dThr = dGrayMuLine + dMedThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		tIp.setThreshold(0, dThr,  ImageProcessor.NO_LUT_UPDATE);
		tImp.updateImage();
		pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(tImp, tIp);
		// get the centroids in microns and convert to px
		fX = (float) m_rt.getValue("XM", 0);
		fX /= ps;
		fY = (float) m_rt.getValue("YM", 0);
		fY /= ps;
		iX = (int) fX;
		iY = (int) fY;
		tImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		lineRoi = tImp.getRoi();
		nPts = lineRoi.getConvexHull().npoints;
		iXpts = lineRoi.getConvexHull().xpoints;
		iYpts = lineRoi.getConvexHull().ypoints;
		xPts = new float[nPts];
		yPts = new float[nPts];
		for (int k=0; k < nPts; k++) {
			xPts[k] = (float) iXpts[k];
			yPts[k] = (float) iYpts[k];		
		}
				
	  linePolyHull = new FloatPolygon(xPts, yPts, nPts);
	  hullRoi = new PolygonRoi(linePolyHull, Roi.POLYGON);
		hullRoi.setStrokeColor(Color.yellow);

		linePolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
		interpolatedHullRoi= new PolygonRoi(linePolyHull.duplicate(), Roi.POLYGON);
		interpolatedHullRoi.setStrokeColor(Color.blue);
		tImp.setTitle("ana-"+m_imp.getTitle());
		tImp.show();
		
		nHullPolyPts=linePolyHull.npoints;
		xh = new double[nHullPolyPts];
		yh = new double[nHullPolyPts];
		double medxr[] = new double[nHullPolyPts];
		double medyr[] = new double[nHullPolyPts];
		double medxl[] = new double[nHullPolyPts];
		double medyl[] = new double[nHullPolyPts];
		for (int i=0; i<nHullPolyPts; i++){
			medxr[i]=-9999999.0;
			medyr[i]=-9999999.0;
			medxl[i]=-9999999.0;
			medyl[i]=-9999999.0;
		}
		
		int nMedPtsL = 0;
		int nMedPtsR = 0;

		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- dGapPx)){
        	//keep - sep from bottom
        	dXt = (xh[i] - fX)*ps;
        	dYt = (yh[i] - fY)*ps;
        	if(dXt > 0){
        		// it is a right side
        		medxr[nMedPtsR]=dXt;
        		medyr[nMedPtsR]=dYt;
        		nMedPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		medxl[nMedPtsL]=dXt;
        		medyl[nMedPtsL]=dYt;
        		nMedPtsL += 1;		
        	}
        }
			}
		}
		
		String strLoXl, strLoYl, strLoXr, strLoYr, strMedXl, strMedYl, strMedXr, strMedYr, strHiXl, strHiYl, strHiXr, strHiYr, strLineOut;
		int nGoodPts = Math.max(nLoPtsL, nLoPtsR);
		nGoodPts = Math.max(nGoodPts, nMedPtsL);
		nGoodPts = Math.max(nGoodPts, nMedPtsR);
		nGoodPts = Math.max(nGoodPts, nHiPtsL);
		nGoodPts = Math.max(nGoodPts, nHiPtsR);
		
    try{
    	File file = new File(strReportPath);
    	if(!file.exists()){
		  	file.createNewFile();
    	}
			boolean bAppend = false;
   
			FileWriter fw = new FileWriter(strReportPath, bAppend);
			fw.write("x.lo.l, y.lo.l, x.lo.r, y.lo.r, x.med.l, y.med.l, x.med.r, y.med.r, x.hi.l, y.hi.l, x.hi.r, y.hi.r\n");
			for(int i=0; i<nGoodPts; i++){
				if(loxl[i] > -99999.0){
					strLoXl = String.format("%.5f, ", loxl[i] );
					strLoYl = String.format("%.5f, ", loyl[i] );		
				} else{
					strLoXl = "  ,";
					strLoYl = "  ,";
				}
				if(loxr[i] > -99999.0){
					strLoXr = String.format("%.5f, ", loxr[i] );
					strLoYr = String.format("%.5f, ", loyr[i] );		
				} else{
					strLoXr = "  , ";
					strLoYr = "  , ";
				}
				if(medxl[i] > -99999.0){
					strMedXl = String.format("%.5f, ", medxl[i] );
					strMedYl = String.format("%.5f, ", medyl[i] );		
				} else{
					strMedXl = "  , ";
					strMedYl = "  , ";
				}
				if(medxr[i] > -99999.0){
					strMedXr = String.format("%.5f, ", medxr[i] );
					strMedYr = String.format("%.5f, ", medyr[i] );		
				} else{
					strMedXr = "  , ";
					strMedYr = "  , ";
				}
				if(hixl[i] > -99999.0){
					strHiXl = String.format("%.5f, ", hixl[i] );
					strHiYl = String.format("%.5f, ", hiyl[i] );		
				} else{
					strHiXl = "  , ";
					strHiYl = "  , ";
				}
				if(hixr[i] > -99999.0){
					strHiXr = String.format("%.5f, ", hixr[i] );
					strHiYr = String.format("%.5f\n", hiyr[i] );		
				} else{
					strHiXr = "  , ";
					strHiYr = "  \n";
				}
				strLineOut = strLoXl + strLoYl + strLoXr + strLoYr + strMedXl + strMedYl + strMedXr + strMedYr + strHiXl + strHiYl + strHiXr + strHiYr;
				fw.write(strLineOut);
			}
			fw.close();
		}
		catch (IOException e){
			e.printStackTrace();
		}
			
		
/*
      filterImage(m_rt, m_imp,
				ps, dMinAreaPx, dMaxAreaPx,
				dMaxIntPx, strReportPath);
            
*/
		
		m_rt.show("analysis of " + iName);
		
	}


}
