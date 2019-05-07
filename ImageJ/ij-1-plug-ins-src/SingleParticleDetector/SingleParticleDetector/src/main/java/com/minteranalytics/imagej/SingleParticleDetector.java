package com.minteranalytics.imagej;
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
* ImageJ plug-in to compute the maximum intrusion distance for
* blobs. One may optionally draw the Convex Hull and the maximum
* intrusion distance for each blob into the overlay.
* 
* Copyright 2012 by John Minter, released under GPL
* You may use this as you see fit. Please cite and send updates and
* suggestions to benefit all of us. A rising tide lifts all ships...
* 
* Created by John Minter 10-Mar-2012
* Revision History
*    Date       Version    Comments
* 10-Mar-2012   0.1.100    Initial prototype. Serious flaw because the
*                          polygon ROI for Convex Hull is undersampled.
*                          Sent query to ImageJ mailing list
*                          
* 11-Mar-2012   0.1.200    Added fix suggested by Wayne Rasband that
*                          used fitSplineForStraightening()
*                          Wayne noted that this had anomalies.
*                          
* 12-Mar-2012   0.1.300    Used another contribution by Wayne:
*                          Roi.getInterpolatedPolygon()
*                          This works better.
*                          Gabriel Landini noted the following issue
*                          with the algorithm:
*                          I think that you need to make sure that you are on
*                          the correct side of the convex hull. Measuring to all
*                          points in the convex hull to find the smallest distance
*                          is not enough. Assume a distorted "B" shape, where the
*                          indent on the right is very deep and closer to the
*                          vertical stroke on the left than to the convex hull on
*                          the side of the indent. You won't get the distance you
*                          expect, but one that goes through the blob (and which
*                          would be erroneous).
*                          
*  14-Mar-2012  0.1.400    Added provisions for loading parameters (see tips
*                          here:  http://fiji.sc/wiki/index.php/PlugIn_Design_Guidelines)
*                          and writing results to a .csv file. Also load/save
*                          preferences and fixed changes to FloatPolygon that
*                          Wayne put in 1.46i25; built under 1.46i30
*                          
*  15-Mar-2012  0.1.500    Added more measurements written to the .csv file.
*                          Designed to be easily processed with R 
*                          
*  17-Mar-12    0.1.600    Adjusted menu text and pref settings so macros worked.
*                          turns out that the first word in a menu must be unique...
*  
*  TO DO:
*  1. Have not encountered case suggested by G. Landini (12-Mar-2012), but need 
*     to consider how to fix this.
*    
*/

public class SingleParticleDetector implements PlugInFilter {
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
	
	private double m_dMinSize = 0., m_dMaxSize=9999999.;

	private ResultsTable m_rt = new ResultsTable();
	private ImagePlus m_imp;
	private boolean  m_bDraw; // draw into the overlay
	private int m_nWidth;
	private int m_nHeight;
	boolean m_IsEdge[];
	
	private String strVersion = "Single Particle Detector v0.1.600";
	
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
		
		String strMaxIntPx = Prefs.getString(".maxInt.px");
		if(strMaxIntPx==null) strMaxIntPx="4.0";
		dMaxIntPx = Double.valueOf(strMaxIntPx);
		
		String strMinAreaPx = Prefs.getString(".minArea.px");
		if(strMinAreaPx==null) strMinAreaPx="10.0";
		double dMinAreaPx = Double.valueOf(strMinAreaPx);
		
		String strMaxAreaPx = Prefs.getString(".maxArea.px");
		if(strMaxAreaPx==null) strMaxAreaPx="999999.0";
		double dMaxAreaPx = Double.valueOf(strMaxAreaPx);
		
		String strDraw = Prefs.getString(".draw.maxInt");
		if(strDraw==null) strDraw="1.0";
		double dDraw = Double.valueOf(strDraw);
		
		// Do the dialog box
        GenericDialog gd = new GenericDialog(strVersion);
        gd.addNumericField("  minArea [sq px]:", dMinAreaPx, 1);
        gd.addNumericField("  maxArea [sq px]:", dMaxAreaPx, 1);
        gd.addNumericField("maxIntrusion [px]:", dMaxIntPx, 1);
        gd.addNumericField(" draw into overlay:", dDraw, 1);
        gd.addStringField ("              path:", strReportDir);
        gd.addStringField ("            report:", strReportFile);
        gd.showDialog();
        if (gd.wasCanceled()) return;
        // 2 - Retrieve parameters from the dialog
        dMinAreaPx = gd.getNextNumber();
        dMaxAreaPx = gd.getNextNumber();
        dMaxIntPx = gd.getNextNumber();
        dDraw = gd.getNextNumber();
        strReportDir = gd.getNextString();
        strReportFile = gd.getNextString();
        
        m_bDraw = true;
        if(dDraw < 1.0 ) m_bDraw = false;
        
        strMinAreaPx = String.format("%.1f", dMinAreaPx );
        strMaxAreaPx = String.format("%.1f", dMaxAreaPx );
	    strMaxIntPx = String.format("%.1f", dMaxIntPx );
        strDraw = String.format("%.1f", dDraw );

        String strReportPath = strReportDir + strReportFile;
        
		Prefs.set("minArea.px", strMinAreaPx);
		Prefs.set("maxArea.px", strMaxAreaPx);
		Prefs.set("maxInt.px", strMaxIntPx);
		Prefs.set("draw.maxInt", strDraw);   
        Prefs.set("rptPath.pth", strReportDir);
		Prefs.set("rptFile.fil", strReportFile);

		Prefs.savePreferences();
		
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
		
		int measurements = Analyzer.getMeasurements(); // defined in Set
														// Measurements dialog
		Analyzer.setMeasurements(0);
		
		// make sure at least area, perimeter, and rect are measured
		
		measurements = Analyzer.AREA + 
				Analyzer.PERIMETER + 
				Analyzer.CIRCULARITY + 
				Analyzer.MEAN + 
				Analyzer.RECT;
		int options = 0;
		Analyzer.setMeasurements(measurements);
		ParticleAnalyzer pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(m_imp, ip);		
		filterImage(m_rt, m_imp,
				ps, dMinAreaPx, dMaxAreaPx,
				dMaxIntPx, strReportPath);
		
		m_rt.show("analysis of " + iName);
		
	}


	void filterImage(ResultsTable objRt, ImagePlus objImp,
			float fCal, double dMinAreaPx, double dMaxAreaPx,
			double dMi, String strRept) {
		Roi objRoi;
		FloatPolygon objFloatPoly;
		FloatPolygon objPolyHull;
		int nParticles = objRt.getCounter();
		int nBlobPolyPts, nHullPolyPts;
		int iXo, iYo;
		float fXo, fYo;
		double dAreaSqPx;
		double dMaxIntr, dEcd, dCirc, dAspect, dMeanGray, dAreaHull, dAreaBlob;
		double dMinD,dBlobX,dBlobY,dHullX,dHullY,dDeltaX, dDeltaY, dDist;

		float[] a = objRt.getColumn(ResultsTable.AREA); // get area measurements
		int iColEcd = objRt.getFreeColumn("ECD");
		int iColBay = objRt.getFreeColumn("Max Intr");
		Overlay overlay = new Overlay();
		m_IsEdge = new boolean [a.length];
		
		for (int ii=0; ii<a.length; ii++){
			m_IsEdge[ii] = false;
		}

		for (int ii=0; ii<a.length; ii++){
			dAreaSqPx = a[ii]/(fCal*fCal);
			dEcd = 2.0 * Math.sqrt(a[ii]/Math.PI);
			if( (dAreaSqPx < dMaxAreaPx) && ( dAreaSqPx > dMinAreaPx) ) {
				fXo = (float) objRt.getValue("BX", ii);
				fXo /= fCal;
				iXo = (int) fXo;
				fYo = (float) objRt.getValue("BY", ii);
				fYo /= fCal;
				iYo = (int) fYo;
				// Let the Wand to find the blob, then get the ROI
				IJ.doWand(iXo, iYo);
				objRoi = objImp.getRoi();
				// get the Convex Hull as a polygon
				// and store the coordinates
				int nPts = objRoi.getConvexHull().npoints;
				int iXpts[] = objRoi.getConvexHull().xpoints;
				int iYpts[] = objRoi.getConvexHull().ypoints;
				float xPts[] = new float[nPts];
				float yPts[] = new float[nPts];
				for (int k=0; k < nPts; k++) {
					xPts[k] = (float) iXpts[k];
					yPts[k] = (float) iYpts[k];		
				}
				
				objPolyHull = new FloatPolygon(xPts, yPts, nPts);
				PolygonRoi hullRoi = new PolygonRoi(objPolyHull, Roi.POLYGON);
				hullRoi.setStrokeColor(Color.yellow);

				objPolyHull = hullRoi.getInterpolatedPolygon(1.0, true); // 1--- pixel spacing
				PolygonRoi interpolatedHullRoi= new PolygonRoi(objPolyHull.duplicate(), Roi.POLYGON);
				interpolatedHullRoi.setStrokeColor(Color.blue);

				nHullPolyPts=objPolyHull.npoints;
				double xh[] = new double[nHullPolyPts];
				double yh[] = new double[nHullPolyPts];
				for (int i=0; i<nHullPolyPts; i++)
					xh[i] = objPolyHull.xpoints[i];
				for (int i=0; i<nHullPolyPts; i++)
					yh[i] = objPolyHull.ypoints[i];
				
				dAreaHull = 0.;
				// compute area of Complex Hull
				for(int i = 0; i <= nHullPolyPts-1; i++) {
					if(i == nHullPolyPts-1)
					{
						dAreaHull += (xh[i]*yh[0])-(xh[0]*yh[i]);
					}
					else
					{
						dAreaHull += (xh[i]*yh[i+1])-(xh[i+1]*yh[i]);
					}
					
				}
				dAreaHull /= 2.0;
				if(dAreaHull < 0) dAreaHull *= -1;
				
				
				
				// get the blob as a polygon
				// and store the coordinates
				Polygon objPolyBlob = objRoi.getPolygon();
				nBlobPolyPts=objPolyBlob.npoints;
				int xb[] = new int[nBlobPolyPts];
				int yb[] = new int[nBlobPolyPts];
				// closest point on the hull...
				int ch[] = new int[nBlobPolyPts];
				for (int i=0; i<nBlobPolyPts; i++) {
					xb[i] = objPolyBlob.xpoints[i];
					// check for edge particles
					if(xb[i] < 1) m_IsEdge[ii] = true;
					if(xb[i] > m_nWidth-2) m_IsEdge[ii] = true;
				}
				for (int i=0; i<nBlobPolyPts; i++) {
					yb[i] = objPolyBlob.ypoints[i];
					// check for edge particles
					if(yb[i] < 1) m_IsEdge[ii] = true;
					if(yb[i] > m_nHeight-2) m_IsEdge[ii] = true;
				}
				
				dAreaBlob = 0.;
				// compute area of blob
				for(int i = 0; i <= nBlobPolyPts-1; i++) {
					if(i == nBlobPolyPts-1)
					{
						dAreaBlob += (xb[i]*yb[0])-(xb[0]*yb[i]);
					}
					else
					{
						dAreaBlob += (xb[i]*yb[i+1])-(xb[i+1]*yb[i]);
					}
					
				}
				dAreaBlob /= 2.0;
				if(dAreaBlob < 0) dAreaBlob *= -1;
				
				double dConcavity = 100.*(dAreaHull-dAreaBlob)/dAreaBlob;
				
				// compute the minimum distance from each
				// point on the blob to the Convex Hull
				double minDist[] = new double[nBlobPolyPts];
				for (int i=0; i<nBlobPolyPts; i++) {
					dMinD = 9999999.0;
					dBlobX = (double) xb[i];
					dBlobY = (double) yb[i];
					for (int j=0; j<nHullPolyPts; j++) {
						dHullX = (double) xh[j];
						dHullY = (double) yh[j];
						dDeltaX = dHullX - dBlobX;
						dDeltaY = dHullY - dBlobY;
						dDist = Math.sqrt(dDeltaX*dDeltaX + dDeltaY*dDeltaY);
						if(dDist < dMinD ) {
							dMinD = dDist;
							ch[i] = j;
						}
					};
					minDist[i]=dMinD;
				}
				dMaxIntr = -1;
				
				int iMinDistPtBlob=0, iMinDistPtHull=0;
				for (int i=0; i<nBlobPolyPts; i++) {
					if(minDist[i] > dMaxIntr) {
						dMaxIntr = minDist[i];
						iMinDistPtBlob = i;
						iMinDistPtHull=ch[i];
					}
				}
				Line line = new Line(xb[iMinDistPtBlob],
						yb[iMinDistPtBlob],
						xh[iMinDistPtHull],
                       yh[iMinDistPtHull]);
				line.setStrokeColor(Color.white );



				String strCl;
				if (dMaxIntr < dMi){
					strCl="s";
				} else {
					strCl="a";
						
				}
				dCirc = objRt.getValue("Circ.", ii);
				dAspect = objRt.getValue("AR", ii);
				dMeanGray = objRt.getValue("Mean", ii);
				
				
				// only output non-edge blobs...		
				if(!m_IsEdge[ii])
				{
					if(m_bDraw) {
						overlay.add(hullRoi);
						overlay.add(interpolatedHullRoi);
						overlay.add(line);			
					}
					objRt.setValue(iColEcd, ii, dEcd);
					objRt.setValue(iColBay, ii, dMaxIntr*fCal);
					appendToFile( strRept, ii, dEcd, strCl, dMaxIntr*fCal, dConcavity, dCirc, dAspect, dMeanGray );
					IJ.showStatus("blob: "+ ii + " Max Intrusion = " + dMaxIntr + ", Processing...");
				}
				IJ.run("Clear", "slice");
			}
		}
		// objRt.updateResults();
		m_imp.setOverlay(overlay);
		IJ.run("Select None");
	}
	
	void appendToFile( String strPath, int iBlob, double dEcd, String strClass,
			double dMaxIntru, double dConcav, double dCir, double dAspR, double dMeanGrayVal  ) {
		try{
			File file = new File(strPath);
			 
    		// if file doesn't exists, then create it
			// and write header
			boolean bWriteHeader=false;
			boolean bAppend = true; 
    		if(!file.exists()){
    			file.createNewFile();
    			bWriteHeader=true;
    		}
 
    		//true = append file
    		FileWriter fw = new FileWriter( strPath, bAppend); 
    	    if(bWriteHeader) {
    	    	fw.write("blob, ecd, class, max.intrusion, pct.concavity, circularity, aspect.ratio, mean.gray\n");	
    	    }
    	    String strBlob = String.format("%d", iBlob);
    	    String strEcd = String.format("%.5f", dEcd );
    	    String strMaxI = String.format("%.5f", dMaxIntru );
    	    String strConcav = String.format("%.5f", dConcav );
    	    String strCirc = String.format("%.5f", dCir );
    	    String strAR = String.format("%.5f", dAspR );
    	    String strID = String.format("%.5f", dMeanGrayVal );
    	    String strLine = strBlob + ", " + 
    	    		strEcd + ", " +  strClass + ", " + strMaxI + ", " + 
    	    		strConcav + ", " + strCirc + ", " +  strAR + ", " + strID + "\n"; 
    	    fw.write(strLine);
    	    fw.close();
		}
		catch (IOException e){
			e.printStackTrace();
		}
	}
}
