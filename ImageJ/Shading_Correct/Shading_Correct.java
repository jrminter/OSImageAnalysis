/**
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * John Minter
 * <jrminter@gmail.com>
 * 
 * Date: 2012/02/17 
 * 
 * Compute a shading correction for a grayscale image and
 * apply it, doing a proper normalization. This converts
 * 8 bit and 32 bit images to 16 bits.
 * 
 * I took many lessons from:
 * 
 * Convert_To_Signed16.java by
 * Jon Jackson <j.jackson@ucl.ac.uk>
 * 
 * and Werner Bailer’s Plug-In Tutorial
 * 
 * 
 * Known problems:
 *   Doesn't handle slices
 */
 
import ij.*;
import ij.process.*;
import ij.measure.*;
import ij.gui.*;
import ij.ImagePlus;
import ij.plugin.filter.*;
import ij.plugin.filter.PlugInFilter;
import ij.plugin.filter.BackgroundSubtracter;
import ij.process.ImageProcessor;

import java.awt.*;


public class Shading_Correct implements PlugInFilter {
	//
	// Define our member variable. Keep them all private.
	// I use the syntax I learned in Visual C++ because it lets one quickly
	// tell the characteristics of the (member) variables.
	//
	private static String strVersion = "Shading Correct v 0.1.100";
	// Radius for RollingBall
	private double m_dBallRadius; 
	// Limit for inverse gain
  private double m_dLimit = 0.05;
  // A debug info variable. Set as appropriate
  private boolean m_bVerbose=false;
  // Need to just create the background
  private boolean m_bCreateBackground=true;
  // The background is light
  private boolean m_bBrightBackground=true;
  // Use a Parabaloid filter
  private boolean m_bUseParaboloid=false;
  // Pre-smooth the image before computing shading
  private boolean m_bDoPresmooth=true;
  // Correct the corners of the shading image
  private boolean m_bCorrectCorners=true;
  // our ImagePlus object
  private ImagePlus m_objImp;
  
  public int setup(String arg, ImagePlus imp) {
		this.m_objImp = imp;
		return DOES_8G + DOES_16 + DOES_32;
	}
	
	public void run(ImageProcessor ip) {
	// 1. Retrieve preferred parameters, if available
	m_dBallRadius = Prefs.getDouble(".sc.BallRadius", 50.0);
	double dVerbose = Prefs.getDouble(".sc.Verbose", 1.0);
	// 2. Prepare the generic dialog
    GenericDialog gd = new GenericDialog(strVersion);
    gd.addNumericField("  ballRadius:", m_dBallRadius, 1);
    gd.addNumericField("     Verbose:", dVerbose, 1);
    gd.showDialog();
    if (gd.wasCanceled()) return;
    
    // 3. - Retrieve parameters from the dialog
    //      check, and save the preferences...
    m_dBallRadius = gd.getNextNumber();
    dVerbose = gd.getNextNumber();
    m_bVerbose = false;
    if(dVerbose != 0.0) m_bVerbose = true;
    Prefs.set("sc.BallRadius", m_dBallRadius);
    Prefs.set("sc.Verbose", dVerbose);
    
    // 4. Get down to business and do the work...	
	
    int iBitDepth = m_objImp.getBitDepth();
    if(m_bVerbose){
      IJ.showMessage(String.format("%d", iBitDepth));
    }
    
    boolean bIsSigned = m_objImp.getCalibration().isSigned16Bit();
		boolean bIsRoi = m_objImp.getRoi()!=null;
		m_objImp.killRoi();
    
    // save the old value for scaling to restore later
		boolean bScaling = ImageConverter.getDoScaling();
    
    ImageConverter.setDoScaling(false);
		double dMax = ip.getMax();
		double dMin = ip.getMin();
		int iSlices = m_objImp.getStackSize();
		if (iSlices == 1) {
      if (iBitDepth == 8) {
				new ImageConverter(m_objImp).convertToGray16();
			}
      if(iBitDepth == 16) {
        if(bIsSigned){
          // we don't want that....
          new ImageConverter(m_objImp).convertToGray32();
          new ImageConverter(m_objImp).convertToGray16();
        }
      }
			// imp.getProcessor().add(32768);
			else {
				new ImageConverter(m_objImp).convertToGray16();
			}
      ip = m_objImp.getProcessor();
      int iW = ip.getWidth();
      int iH = ip.getHeight();
      ImagePlus objImpWork = IJ.createImage("My new image",
         "16-bit black", iW, iH, 1);  
      objImpWork.show();
      short[] pix_new = (short[])objImpWork.getProcessor().getPixels();
      short[] pix_old = (short[])ip.getPixels();
      for(int y=0; y<iH; y++){
        for(int x=0; x<iW; x++){
          pix_new[y*iW+x] = pix_old[y*iW+x];
        }
      }
      objImpWork.getProcessor().setPixels(pix_new);
      
      // Now compute the shading image
      
      BackgroundSubtracter objBks = new BackgroundSubtracter();
      objBks.rollingBallBackground(ip,
        m_dBallRadius,
        m_bCreateBackground,
        m_bBrightBackground,
        m_bUseParaboloid,
        m_bDoPresmooth,
        m_bCorrectCorners);
      dMax = ip.getMax();
      dMin = ip.getMin();
      
      double dVal, dOrig;
      int iVal;
      short sVal;
    
      
      pix_old = (short[])ip.getPixels(); // the shaded image
      for(int y=0; y<iH; y++){
        for(int x=0; x<iW; x++){
          dVal = (double)  pix_old[y*iW+x];
          dVal = dVal/dMax;
          if (dVal < m_dLimit) dVal = m_dLimit;
          dVal = 1.0/dVal; // the normalization coefficient
          dOrig = (double) pix_new[y*iW+x];
          dVal = dVal * dOrig;
          dVal = dVal + 0.5;
          dVal = Math.floor(dVal);
          if (dVal < 0.) dVal = 0.;
          if (dVal > 65535.) dVal = 65535.;
          
          if(bIsSigned){
            // get rid of the sign bit. Thanks to Werner Bailer
            iVal = ((int) dVal) & 0xffff;
          }
          else {
            iVal = ((int) dVal);
          }
          sVal = (short) iVal;
          pix_old[y*iW+x]= sVal;
        }
      }
      ip.setPixels(pix_old); // write the corrected intensity
      ip.resetMinAndMax();
      // update 
      m_objImp.updateAndDraw();
     
      
      if(!m_bVerbose){
        objImpWork.close(); // close the work image
      }
    }
    else{
      IJ.showMessage("This does not yet support stacks...");
    }
	}
}
