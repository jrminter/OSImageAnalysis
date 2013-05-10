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
* 
* Revision History
*    Date       Version    Comments
* 2013-05-08   0.1.100     Initial prototype.
* 2013-05-09   0.1.200     First refactoring 
*
*  TO DO:
*  1. need to check results and find out how to close some windows
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

	private boolean m_bVerbose; // write log messages
	
	private double m_dMinAreaPx = 5.;
	private double m_dMaxAreaPx=9999999.;
	private double m_dGapPx=1.0;
	private double m_dLoThrFr=0.20;
	private double m_dMedThrFr=0.50;
	private double m_dHiThrFr=0.75;

	private int m_nWidth;
	private int m_nHeight;

	private String strVersion = "Analyze Line v. 0.1.200";
	private String m_strReportPath = "C:\\report.csv";

	private ResultsTable m_rt = new ResultsTable();
	private ResultsTable m_rtLoL = new ResultsTable();
	private ResultsTable m_rtLoR = new ResultsTable();
	private ResultsTable m_rtMedL = new ResultsTable();
	private ResultsTable m_rtMedR = new ResultsTable();
	private ResultsTable m_rtHiL = new ResultsTable();
	private ResultsTable m_rtHiR = new ResultsTable();
	
	private ImagePlus m_imp;

	
	public int setup(String arg, ImagePlus imp) {
		// Ask to process stacks.
		// SNAPSHOT: We always need a snapshot, also if not needed for
		// undo (e.g. in case of a stack).
		m_imp=imp;
		return IJ.setupDialog(imp, DOES_8G | DOES_16 | SNAPSHOT);
	}

	public boolean getParameters(){
			// 1 - Ask for parameters:
		String strPrefsDir = Prefs.getPrefsDir();
		
		String strReportDir = Prefs.getString(".rptPath.pth");
		if(strReportDir==null) strReportDir="replace";
		
		String strReportFile = Prefs.getString(".rptFile.fil");
		if(strReportFile==null) strReportFile="me";
		
		String strMinAreaPx = Prefs.getString(".minArea.px");
		if(strMinAreaPx==null) strMinAreaPx="10.0";
		m_dMinAreaPx = Double.valueOf(strMinAreaPx);
		
		String strMaxAreaPx = Prefs.getString(".maxArea.px");
		if(strMaxAreaPx==null) strMaxAreaPx="999999.0";
		m_dMaxAreaPx = Double.valueOf(strMaxAreaPx);

		String strGapPx = Prefs.getString(".gap.px");
		if(strGapPx==null) strGapPx="5.0";
	  m_dGapPx = Double.valueOf(strGapPx);

		String strLoThrFr = Prefs.getString(".loThr.fr");
		if(strLoThrFr==null) strLoThrFr="0.25";
		m_dLoThrFr = Double.valueOf(strLoThrFr);

	  String strMedThrFr = Prefs.getString(".medThr.fr");
		if(strMedThrFr==null) strMedThrFr="0.50";
		m_dMedThrFr = Double.valueOf(strMedThrFr);

	  String strHiThrFr = Prefs.getString(".hiThr.fr");
		if(strHiThrFr==null) strHiThrFr="0.75";
		double m_dHiThrFr = Double.valueOf(strHiThrFr);
		
		
		String strVerbose = Prefs.getString(".line.verbose");
		if(strVerbose==null) strVerbose="1.0";
		double dVerbose = Double.valueOf(strVerbose);
		
		// Do the dialog box
		GenericDialog gd = new GenericDialog(strVersion);
		gd.addNumericField("   min Area [sq px]:", m_dMinAreaPx, 1);
		gd.addNumericField("   max Area [sq px]:", m_dMaxAreaPx, 1);
		gd.addNumericField("top/bottom gap [px]:", m_dGapPx, 1);
		gd.addNumericField("  Lo Threshold [fr]:", m_dLoThrFr, 2);
		gd.addNumericField(" Med Threshold [fr]:", m_dMedThrFr, 2);
		gd.addNumericField("  Hi Threshold [fr]:", m_dHiThrFr, 2);
		gd.addNumericField("      log messages :", dVerbose, 1);
		gd.addStringField ("              path :", strReportDir);
		gd.addStringField ("            report :", strReportFile);
		gd.showDialog();
		if (gd.wasCanceled()) return false;
    
    // 2 - Retrieve parameters from the dialog     
    m_dMinAreaPx = gd.getNextNumber();
    m_dMaxAreaPx = gd.getNextNumber();
    m_dGapPx = gd.getNextNumber();
    m_dLoThrFr = gd.getNextNumber();
    m_dMedThrFr = gd.getNextNumber();
    m_dHiThrFr = gd.getNextNumber();
    dVerbose = gd.getNextNumber();
    strReportDir = gd.getNextString();
    strReportFile = gd.getNextString();
        
    m_bVerbose = true;
    if(dVerbose < 1.0 ) m_bVerbose = false;
        
    strMinAreaPx = String.format("%.1f", m_dMinAreaPx );
    strMaxAreaPx = String.format("%.1f", m_dMaxAreaPx );
    strGapPx     = String.format("%.1f", m_dGapPx );
    strLoThrFr   = String.format("%.2f", m_dLoThrFr );
    strMedThrFr  = String.format("%.2f", m_dMedThrFr );
    strHiThrFr   = String.format("%.2f", m_dHiThrFr );

    strVerbose = String.format("%.1f", dVerbose );
    
    Prefs.set("minArea.px", strMinAreaPx);
		Prefs.set("maxArea.px", strMaxAreaPx);
		Prefs.set("gap.px", strGapPx);
		Prefs.set("loThr.fr", strLoThrFr);
		Prefs.set("medThr.fr", strMedThrFr);
		Prefs.set("hiThr.fr", strHiThrFr);
		Prefs.set("line.verbose", strVerbose);   
    Prefs.set("rptPath.pth", strReportDir);
		Prefs.set("rptFile.fil", strReportFile);

		m_strReportPath = strReportDir + strReportFile;

		Prefs.savePreferences();
		return true;
	}

	public ParticleAnalyzer setupAnalyzer(){
		int measurements = Analyzer.getMeasurements(); // defined in Set Measurements dialog
		Analyzer.setMeasurements(0);
		// make sure at least area, cennter of mass, and rect are measured		
		measurements = Analyzer.AREA + 
				Analyzer.CENTER_OF_MASS + 
				Analyzer.MEAN + 
				Analyzer.RECT;
		int options = 0;
		Analyzer.setMeasurements(measurements);
		ParticleAnalyzer pa = new ParticleAnalyzer(options,
				measurements, m_rt,
				m_dMinAreaPx, m_dMaxAreaPx);
	  return pa;	
	}

	public void analyzeBoundary(ImagePlus workImp, double dThresh, double space, ResultsTable rtL, ResultsTable rtR ){
		ImageProcessor tIp = workImp.getProcessor();
		tIp.setThreshold(0, dThresh,  ImageProcessor.NO_LUT_UPDATE);
		workImp.updateImage();
		ParticleAnalyzer pa = setupAnalyzer();
		pa.analyze(workImp, tIp);
		// get the centroids in microns and convert to px
		float fX = (float) m_rt.getValue("XM", 0);
		fX /= space;
		float fY = (float) m_rt.getValue("YM", 0);
		fY /= space;
		int iX = (int) fX;
		int iY = (int) fY;
		workImp.show();
		IJ.doWand(iX, iY);
		m_rt.deleteRow(0);

		Roi lineRoi = workImp.getRoi();
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
		workImp.setTitle("ana-"+m_imp.getTitle());
		workImp.show();
		
		int nHullPolyPts=linePolyHull.npoints;
		double xh[] = new double[nHullPolyPts];
		double yh[] = new double[nHullPolyPts];
		
		int nPtsL = 0;
		int nPtsR = 0;

		for (int i=0; i<nHullPolyPts; i++){
			xh[i] = linePolyHull.xpoints[i];
			yh[i] = linePolyHull.ypoints[i];
			if (yh[i] > m_dGapPx){
				// keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- m_dGapPx)){
        	//keep - sep from bottom
        	double dXt = (xh[i] - fX)*space;
        	double dYt = (yh[i] - fY)*space;
        	if(dXt > 0){
        		// it is a right side
        		rtR.setValue("X", nPtsR, dXt);
        		rtR.setValue("Y", nPtsR, dYt);
        		nPtsR += 1;		
        	}
        	else{
        		// it is a left side
        		rtL.setValue("X", nPtsL, dXt);
        		rtL.setValue("Y", nPtsL, dYt);
        		nPtsL += 1;		
        	}
        }
			}
		}
		rtR.updateResults();
		rtL.updateResults();
	}

	public void writeResults(){
		String strLoXl, strLoYl, strLoXr, strLoYr;
		String strMedXl, strMedYl, strMedXr, strMedYr;
		String strHiXl, strHiYl, strHiXr, strHiYr, strLineOut;

    int nPtsLoL  = m_rtLoL.getCounter();
    int nPtsLoR  = m_rtLoR.getCounter();
    int nPtsMedL = m_rtMedL.getCounter();
    int nPtsMedR = m_rtMedR.getCounter();
    int nPtsHiL  = m_rtHiL.getCounter();
    int nPtsHiR  = m_rtHiR.getCounter();
		
		int nGoodPts = Math.max(nPtsLoL, nPtsLoR);
		nGoodPts = Math.max(nGoodPts, nPtsMedL);
		nGoodPts = Math.max(nGoodPts, nPtsMedR);
		nGoodPts = Math.max(nGoodPts, nPtsHiL);
		nGoodPts = Math.max(nGoodPts, nPtsHiR);
		
    try{
    	File file = new File(m_strReportPath);
    	if(!file.exists()){
		  	file.createNewFile();
    	}
			boolean bAppend = false;
   
			FileWriter fw = new FileWriter(m_strReportPath, bAppend);
			fw.write("x.lo.l, y.lo.l, x.lo.r, y.lo.r, x.med.l, y.med.l, x.med.r, y.med.r, x.hi.l, y.hi.l, x.hi.r, y.hi.r\n");
			for(int i=0; i<nGoodPts; i++){
				if(i < nPtsLoL ){
					strLoXl = String.format("%.5f, ", m_rtLoL.getValue("X",i ));
					strLoYl = String.format("%.5f, ", m_rtLoL.getValue("Y",i ));
				} else{
					strLoXl = "  ,";
					strLoYl = "  ,";
				}
				if(i < nPtsLoR){
					strLoXr = String.format("%.5f, ", m_rtLoL.getValue("X",i ));
					strLoYr = String.format("%.5f, ", m_rtLoL.getValue("Y",i ));
				} else{
					strLoXr = "  , ";
					strLoYr = "  , ";
				}
				if(i < nPtsMedL ){
					strMedXl = String.format("%.5f, ", m_rtMedL.getValue("X",i ));
					strMedYl = String.format("%.5f, ", m_rtMedL.getValue("Y",i ));
				} else{
					strMedXl = "  ,";
					strMedYl = "  ,";
				}
				if(i < nPtsMedR){
					strMedXr = String.format("%.5f, ", m_rtMedL.getValue("X",i ));
					strMedYr = String.format("%.5f, ", m_rtMedL.getValue("Y",i ));
				} else{
					strMedXr = "  , ";
					strMedYr = "  , ";
				}
				if(i < nPtsHiL ){
					strHiXl = String.format("%.5f, ", m_rtHiL.getValue("X",i ));
					strHiYl = String.format("%.5f, ", m_rtHiL.getValue("Y",i ));
				} else{
					strHiXl = "  ,";
					strHiYl = "  ,";
				}
				if(i < nPtsHiR){
					strHiXr = String.format("%.5f, ", m_rtHiL.getValue("X",i ));
					strHiYr = String.format("%.5f\n ", m_rtHiL.getValue("Y",i ));
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
		
		
	}

	public void run(ImageProcessor ip) {
		if (IJ.versionLessThan("1.46i"))
			return;

		if(!getParameters()) return;
	
		// First some house-keeping...	
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


		// 4. Now measure background ROIS intensities on a duplicate
		ImagePlus tImp = m_imp.duplicate();
		ImageProcessor tIp = tImp.getProcessor();
		IJ.setAutoThreshold(tImp, "Default dark");

		ParticleAnalyzer pa = setupAnalyzer();
		pa.analyze(tImp, tIp);
		double dGrayMuL = m_rt.getValue("Mean", 0);
		double dGrayMuR = m_rt.getValue("Mean", 1);
		double dGrayMuBkg = (dGrayMuL + dGrayMuR)/2.0;
		if(m_bVerbose) IJ.log("mean gray bkg " + dGrayMuBkg);
		m_rt.deleteRow(0);
		m_rt.deleteRow(0);
		tImp.close();

		// 5. Now measure line ROI intensity on a duplicate
		tImp = m_imp.duplicate();
		tIp = tImp.getProcessor();
		IJ.setAutoThreshold(tImp, "Default");
		// pa = setupAnalyzer();
		pa.analyze(tImp, tIp);
		double dGrayMuLine = m_rt.getValue("Mean", 0);
		if(m_bVerbose) IJ.log("mean gray line " + dGrayMuLine);
		m_rt.deleteRow(0);
		tImp.close();

		double dDeltaGray = dGrayMuBkg - dGrayMuLine;

	  // 6. Analyse the line for the low delta fraction

		double dThr = dGrayMuLine + m_dLoThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		analyzeBoundary(tImp, dThr, ps, m_rtLoL, m_rtLoR );
		if(m_bVerbose) IJ.log("nLoPtsL " + m_rtLoL.getCounter());
		if(m_bVerbose) IJ.log("nLoPtsR " + m_rtLoR.getCounter());
		tImp.close();
		
	  // 7. Analyse the line for the high delta fraction

		dThr = dGrayMuLine + m_dHiThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		analyzeBoundary(tImp, dThr, ps, m_rtHiL, m_rtHiR );
		if(m_bVerbose) IJ.log("nHiPtsL " + m_rtHiL.getCounter());
		if(m_bVerbose) IJ.log("nHiPtsR " + m_rtHiR.getCounter());


		// 8.  Analyse the line for the medium delta fraction

		dThr = dGrayMuLine + m_dMedThrFr*dDeltaGray;
		tImp = m_imp.duplicate();
		analyzeBoundary(tImp, dThr, ps, m_rtMedL, m_rtMedR );
		if(m_bVerbose) IJ.log("nMedPtsL " + m_rtMedL.getCounter());
		if(m_bVerbose) IJ.log("nMedPtsR " + m_rtMedR.getCounter());
		tImp.show();
		// m_rtMedL.show("L med of " + iName);

		writeResults();

	
/*
      filterImage(m_rt, m_imp,
				ps, m_dMinAreaPx, m_dMaxAreaPx,
				dMaxIntPx, strReportPath);
            
*/
		
		// m_rt.show("analysis of " + iName);
		
	}


}
