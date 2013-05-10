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
* 2013-05-10   0.1.300     cleaned up windows and variable names
*                          and did a better job of commenting
* 2013-05-10   0.1.400     Used float polygon from ROI rather than
*                          Convex hull to get rid of a nasty bug
*                          where only half the polygon was transferred...
*                          Also draw final overlay into image.
*  TO DO:
*  1. need to check results with R. First test is not too bad
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

  // will allocate this later
  private PolygonRoi m_finalRoi;
  
  private ImagePlus m_imp;

  
  public int setup(String arg, ImagePlus imp) {
    // Ask to process stacks.
    // SNAPSHOT: We always need a snapshot, also if not needed for
    // undo (e.g. in case of a stack).
    m_imp=imp;
    return IJ.setupDialog(imp, DOES_8G | DOES_16 | SNAPSHOT);
  }

  public boolean getParameters(){
    /*
    * Recall last parametersfrom preference file, load dialog,
    * get current parameters, populate member variables,
    * and save to preferences as new defaults
    */
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
    /*
     * Create a particle analyzer to make the desired measurements
     * (area, center_of_mass, mean value, and the bounding box)
     * and return it to do the work...
     */
    int measurements = Analyzer.getMeasurements();
    Analyzer.setMeasurements(0);  
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

  public void analyzeLineEdges(ImagePlus workImp, double dThresh, double dPxCal, ResultsTable rtL, ResultsTable rtR ){
    /*
     * Detect and measure the points on the left and right edges of the supplied line segment
     * using the supplied gray level threshold. Return the coordinates of the left and right
     * edges as individual result tables. 
     */
    ImageProcessor tIp = workImp.getProcessor();
    tIp.setThreshold(0, dThresh,  ImageProcessor.NO_LUT_UPDATE);
    workImp.updateImage();
    ParticleAnalyzer pa = setupAnalyzer();
    pa.analyze(workImp, tIp);
    // get the centroids in microns and convert to px
      double dX = m_rt.getValue("XM", 0);
    dX /= dPxCal;
    if(m_bVerbose) IJ.log("dX = " + dX);
    double dY = m_rt.getValue("YM", 0);
    dY /= dPxCal;
    int iX = (int) dX;
    int iY = (int) dY;
    if(m_bVerbose) IJ.log("dY = " + dY);
    workImp.show();
    IJ.doWand(iX, iY);
    m_rt.deleteRow(0);

    Roi theROI = workImp.getRoi();
    FloatPolygon interpPoly = theROI.getInterpolatedPolygon(1.0, false);
    PolygonRoi interpRoi = new PolygonRoi(interpPoly, Roi.POLYGON);
    FloatPolygon polyFloat = interpRoi.getFloatPolygon();
    interpRoi.setStrokeColor(Color.red);
    workImp.setTitle("ana-"+m_imp.getTitle());
    workImp.show();
    
    int nPts=polyFloat.npoints;
    double xh[] = new double[nPts];
    double yh[] = new double[nPts];
    
    int nPtsL = 0;
    int nPtsR = 0;

    for (int i=0; i<nPts; i++){
      xh[i] = polyFloat.xpoints[i];
      yh[i] = polyFloat.ypoints[i];
      if (yh[i] > m_dGapPx){
        // keep - sep from top
        if (yh[i] < ((double)( m_nHeight)- m_dGapPx)){
          //keep - sep from bottom
          double dXt = (xh[i] - dX)*dPxCal;
          double dYt = (yh[i] - dY)*dPxCal;
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
    m_finalRoi = interpRoi;
    rtR.updateResults();
    rtL.updateResults();
  }

  public void writeResultsFile(){
    /*
     * Extract the line edges from the six result tables and
     * write them to a comma-delimited text file (.csv) suitable
     * for input into R. Nota Bene: these lines may be of different
     * lengths, so pad the bottom of short lines with spaces
     * that R wil interpret as NA values. 
     */
    String strLoXl, strLoYl, strLoXr, strLoYr;
    String strMedXl, strMedYl, strMedXr, strMedYr;
    String strHiXl, strHiYl, strHiXr, strHiYr, strLineOut;

    int nPtsLoL  = m_rtLoL.getCounter();
    int nPtsLoR  = m_rtLoR.getCounter();
    int nPtsMedL = m_rtMedL.getCounter();
    int nPtsMedR = m_rtMedR.getCounter();
    int nPtsHiL  = m_rtHiL.getCounter();
    int nPtsHiR  = m_rtHiR.getCounter();

    // find the longest line
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
          strLoXr = String.format("%.5f, ", m_rtLoR.getValue("X",i ));
          strLoYr = String.format("%.5f, ", m_rtLoR.getValue("Y",i ));
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
          strMedXr = String.format("%.5f, ", m_rtMedR.getValue("X",i ));
          strMedYr = String.format("%.5f, ", m_rtMedR.getValue("Y",i ));
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
          strHiXr = String.format("%.5f, ", m_rtHiR.getValue("X",i ));
          strHiYr = String.format("%.5f\n ", m_rtHiR.getValue("Y",i ));
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
    /*
     * This actually does the heavy lifting... Note that we need to
     * generate duplicate image processors for the intermediate
     * measurements.
     */
    Overlay overlay = new Overlay();
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
    double dPixWidth = cal.pixelWidth;

    /*
     * Now detect the two background ROIs on a duplicate
     * image processor, measure the mean gray level of each,
     * and store the average gray level for the background.
     */
    ImagePlus tImp = m_imp.duplicate();
    ImageProcessor tIp = tImp.getProcessor();
    IJ.setAutoThreshold(tImp, "Default dark");

    ParticleAnalyzer pa = setupAnalyzer();
    pa.analyze(tImp, tIp);
    double dGrayMuL = m_rt.getValue("Mean", 0);
    double dGrayMuR = m_rt.getValue("Mean", 1);
    double dGrayMuBkg = (dGrayMuL + dGrayMuR)/2.0;
    if(m_bVerbose) IJ.log("mean gray bkg " + dGrayMuBkg);
    // clean up
    m_rt.deleteRow(0);
    m_rt.deleteRow(0);
    tImp.close();

    /*
     * Now detect the line ROI on a duplicate
     * image processor, measure the mean gray,
     * and store the average gray level for the line.
     * Store the mean difference in gray level between
     * line and background for subsequent threshold
     * operations.
     */
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

    /*
     * Now detect the line ROI on a duplicate image processor
     * using the low delta fraction threshold, 
     * and measure the coordinates of the two edges, storing
     * the results in the appropriate result tables.
     */

    double dThr = dGrayMuLine + m_dLoThrFr*dDeltaGray;
    tImp = m_imp.duplicate();
    analyzeLineEdges(tImp, dThr, dPixWidth, m_rtLoL, m_rtLoR );
    if(m_bVerbose) IJ.log("nLoPtsL " + m_rtLoL.getCounter());
    if(m_bVerbose) IJ.log("nLoPtsR " + m_rtLoR.getCounter());
    tImp.close();
    
    /*
     * Now detect the line ROI on a duplicate image processor
     * using the high delta fraction threshold, 
     * and measure the coordinates of the two edges, storing
     * the results in the appropriate result tables.
     */

    dThr = dGrayMuLine + m_dHiThrFr*dDeltaGray;
    tImp = m_imp.duplicate();
    analyzeLineEdges(tImp, dThr, dPixWidth, m_rtHiL, m_rtHiR );
    if(m_bVerbose) IJ.log("nHiPtsL " + m_rtHiL.getCounter());
    if(m_bVerbose) IJ.log("nHiPtsR " + m_rtHiR.getCounter());
    tImp.close();


    /*
     * Now detect the line ROI on a duplicate image processor
     * using the medium delta fraction threshold, 
     * and measure the coordinates of the two edges, storing
     * the results in the appropriate result tables.
     */

    dThr = dGrayMuLine + m_dMedThrFr*dDeltaGray;
    tImp = m_imp.duplicate();
    analyzeLineEdges(tImp, dThr, dPixWidth, m_rtMedL, m_rtMedR );
    if(m_bVerbose) IJ.log("nMedPtsL " + m_rtMedL.getCounter());
    if(m_bVerbose) IJ.log("nMedPtsR " + m_rtMedR.getCounter());

    writeResultsFile();

    /* 
     *  Clean up empty results window
     */
    TextWindow win = m_rt.getResultsWindow(); 
    if (win!=null) win.close();
    tImp.close();
    m_imp.show();
    overlay.add(m_finalRoi);
    m_imp.setOverlay(overlay);
    m_imp.updateAndDraw();
  }
}
