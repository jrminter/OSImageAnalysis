import ij.*;
import ij.plugin.*;
import ij.plugin.filter.*;
import ij.plugin.Animator.*;
import ij.process.*;
import ij.gui.*;
import ij.measure.*;
import ij.text.*;
import java.util.*;
import java.awt.*;
import java.awt.event.*;
import ij.plugin.*;

/*
 * Adapted from shape descriptor
 */

public class Single_Particle_Detector implements PlugInFilter {
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
	
	public int setup(String arg, ImagePlus imp) {
		// Ask to process stacks.
	    // SNAPSHOT: We always need a snapshot, also if not needed for
	    // undo (e.g. in case of a stack).
		m_imp=imp;
		return IJ.setupDialog(imp, DOES_8G | DOES_16 | SNAPSHOT);
	   }


	public void run(ImageProcessor ip) {
		if (IJ.versionLessThan("1.43d"))
			return;

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
		
		// make sure area, perimeter, and rect are measured
		
		measurements = Analyzer.AREA + Analyzer.PERIMETER + Analyzer.RECT; 
		int options = 0;
		Analyzer.setMeasurements(measurements);
		ParticleAnalyzer pa = new ParticleAnalyzer(options, measurements, m_rt,
				m_dMinSize, m_dMaxSize);
		pa.analyze(m_imp, ip);		
		filterImage(m_rt, m_imp, ps);
		m_rt.show("analysis of " + iName);
		
	}


	void filterImage(ResultsTable objRt, ImagePlus objImp, float fCal) {
		Roi objRoi;
		FloatPolygon objFloatPoly;
		Polygon objPolyHull;
		int nParticles = objRt.getCounter();
		int nBlobPolyPts, nHullPolyPts;
		int iXo, iYo;
		float fXo, fYo;
		float fAreaSqPx;
		double dMaxIntr, dEcd;
		double dMinD,dBlobX,dBlobY,dHullX,dHullY,dDeltaX, dDeltaY, dDist;

		float[] a = objRt.getColumn(ResultsTable.AREA); // get area measurements
		int iColEcd = objRt.getFreeColumn("ECD");
		int iColBay = objRt.getFreeColumn("Max Intr");

		for (int ii=0; ii<a.length; ii++){
			fAreaSqPx = a[ii]/(fCal*fCal);
			dEcd = 2.0 * Math.sqrt(a[ii]/Math.PI);
			if( fAreaSqPx < 5000. || fAreaSqPx > 50.) {
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
				objPolyHull = objRoi.getConvexHull();
				// Thanks to Wayne Rasband for the next 3 lines...
				PolygonRoi hullRoi = new PolygonRoi(objPolyHull, Roi.POLYGON);
				hullRoi.fitSplineForStraightening();
				objPolyHull = hullRoi.getPolygon();
				nHullPolyPts=objPolyHull.npoints;
				int xh[] = new int[nHullPolyPts];
				int yh[] = new int[nHullPolyPts];
				for (int i=0; i<nHullPolyPts; i++)
					xh[i] = objPolyHull.xpoints[i];
				for (int i=0; i<nHullPolyPts; i++)
					yh[i] = objPolyHull.ypoints[i];
				
				// get the blob as a polygon 
				// and store the coordinates
				Polygon objPolyBlob = objRoi.getPolygon();
				nBlobPolyPts=objPolyBlob.npoints;
				int xb[] = new int[nBlobPolyPts];
				int yb[] = new int[nBlobPolyPts];
				// closest point on the hull...
				int ch[] = new int[nBlobPolyPts];
				for (int i=0; i<nBlobPolyPts; i++)
					xb[i] = objPolyBlob.xpoints[i];
				for (int i=0; i<nBlobPolyPts; i++)
					yb[i] = objPolyBlob.ypoints[i];
				
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
				objImp.getProcessor().drawLine(xb[iMinDistPtBlob],
						yb[iMinDistPtBlob],
						xh[iMinDistPtHull],
                        yh[iMinDistPtHull]);

				objRt.setValue(iColEcd, ii, dEcd);
				objRt.setValue(iColBay, ii, dMaxIntr*fCal);
				
				IJ.showStatus("blob: "+ ii + " Max Intrusion = " + dMaxIntr + ", Processing...");
				// IJ.run("Clear", "slice");
			}
		}
		// objRt.updateResults();
		IJ.run("Select None");
	}

	


	float[][] trimArray(float[][] tArray, int n) {
		float[][] newArray = new float[tArray.length][n];
		for (int i = 0; i < n; i++)
			for (int ii = 0; ii < tArray.length; ii++)
				newArray[ii][i] = tArray[ii][i];
		return newArray;
	}



	double sqr(double x) {
		return x * x;
	}


}
