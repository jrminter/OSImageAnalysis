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
 * Scale a 16 bit grayscale image to an 8 bit
 * 
 * I took many lessons from:
 * 
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


public class Scale_To8 implements PlugInFilter {
    // our ImagePlus object
  private ImagePlus m_objImp;
  
  public int setup(String arg, ImagePlus imp) {
		this.m_objImp = imp;
		return DOES_16 + DOES_32;
	}
  
  public void run(ImageProcessor ip) {
    int iBitDepth = m_objImp.getBitDepth();
    Calibration objCalib = m_objImp.getCalibration();
    boolean bIsRoi = m_objImp.getRoi()!=null;
		m_objImp.killRoi();
    
    // save the old value for scaling to restore later
		boolean bScaling = ImageConverter.getDoScaling();
    
    ImageConverter.setDoScaling(false);
		double dMax = ip.getMax();
		double dMin = ip.getMin();
		double dFactor = 255.0/(dMax-dMin);
		int iSlices = m_objImp.getStackSize();
		if (iSlices == 1) {
			ip = m_objImp.getProcessor();
      int iW = ip.getWidth();
      int iH = ip.getHeight();
      String strName = m_objImp.getTitle() + "-8b";
      
      ImagePlus objImpWork = IJ.createImage(strName,
         "8-bit black", iW, iH, 1);  
      objImpWork.show();
      byte[] pix_new = (byte[])objImpWork.getProcessor().getPixels();
      
			
			double dVal, dOrig;
      int iVal;
      byte byVal;
      if (iBitDepth == 32) {
				double[] pix_old = (double[])ip.getPixels();	
				for(int y=0; y<iH; y++){
					for(int x=0; x<iW; x++){
						dVal = (double)  pix_old[y*iW+x];
						dVal -= dMin;
						dVal *= dFactor;
						dVal = dVal + 0.5;
						dVal = Math.floor(dVal);
						if (dVal < 0.) dVal = 0.;
						if (dVal > 255.) dVal = 255.;
						iVal = ((int) dVal) & 0xff;
						byVal = (byte) iVal;
						pix_new[y*iW+x]= byVal;     
					}
				}
				objImpWork.getProcessor().setPixels(pix_new); // write the corrected intensity
			}
			else{
				short[] pix_old = (short[])ip.getPixels();	
				for(int y=0; y<iH; y++){
					for(int x=0; x<iW; x++){
						dVal = (double)  pix_old[y*iW+x];
						dVal -= dMin;
						dVal *= dFactor;
						dVal = dVal + 0.5;
						dVal = Math.floor(dVal);
						if (dVal < 0.) dVal = 0.;
						if (dVal > 255.) dVal = 255.;
						iVal = ((int) dVal) & 0xff;
						byVal = (byte) iVal;
						pix_new[y*iW+x]= byVal;     
					}
				}
				objImpWork.getProcessor().setPixels(pix_new); // write the corrected intensity
			}
			//show the image
		  objImpWork.updateAndDraw();
		  objImpWork.setCalibration(objCalib);
      // finally, let's adjust the contrast
     objImpWork.getProcessor().resetMinAndMax();	
	  }
	  else{
      IJ.showMessage("This does not yet support stacks...");
    }
  }
		
}
