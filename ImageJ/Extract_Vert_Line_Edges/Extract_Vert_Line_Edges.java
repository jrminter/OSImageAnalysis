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
 * Date: 2013/04/17 
 * 
 * Find the left and right line edges for subsequent processing
 * in R.
 *
 * Known problems:
 *   TBD
 */
 
import ij.*;
import ij.process.*;
import ij.measure.*;
import ij.gui.*;
import ij.ImagePlus;
import ij.plugin.filter.*;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

import java.awt.*;

public class Extract_Vert_Line_Edges implements PlugInFilter {
  //
  // Define our member variable. Keep them all private.
  // I use the syntax I learned in Visual C++ because it lets one quickly
  // tell the characteristics of the (member) variables.
  //
  private static String strVersion = "Extract Vertical Line Edges v 0.1.100";
  
  
  // our ImagePlus object
  private ImagePlus m_objImp;
  // Fraction of jump for threshold
  private double m_dDeltaFrac = 0.5;
  // Fraction of image width for bkg detect from edges
  private double m_dBkgWidthFrac = 0.15;
  // Fraction of image width for line detect from center
  private double m_dLineWidthFrac = 0.15;
  
  public int setup(String arg, ImagePlus imp) {
    this.m_objImp = imp;
    return DOES_8G + DOES_16 + DOES_32;
  }
  
  public void run(ImageProcessor ip) {
    // 1. Retrieve preferred parameters, if available
    m_dDeltaFrac = Prefs.getDouble(".evl.DeltaFrac", 0.50);
    m_dBkgWidthFrac = Prefs.getDouble(".evl.BkgWidthFrac", 0.10);
    m_dLineWidthFrac = Prefs.getDouble(".evl.LineWidthFrac", 0.10);
  
    // 2. Prepare the generic dialog
    GenericDialog gd = new GenericDialog(strVersion);
    gd.addNumericField(" edgeDeltaFrac: ", m_dDeltaFrac, 2);
    gd.addNumericField("  bkgWidthFrac: ", m_dBkgWidthFrac, 2);
    gd.addNumericField(" lineWidthFrac: ", m_dLineWidthFrac, 2);
    gd.showDialog();
    if (gd.wasCanceled()) return;
  
    // 3. - Retrieve parameters from the dialog
    //      check, and save the preferences...
    m_dDeltaFrac = gd.getNextNumber();
    m_dBkgWidthFrac = gd.getNextNumber();
    m_dLineWidthFrac = gd.getNextNumber();
    // save them
    Prefs.set(".evl.DeltaFrac", m_dDeltaFrac);
    Prefs.set(".evl.BkgWidthFrac", m_dBkgWidthFrac);
    Prefs.set(".evl.LineWidthFrac", m_dLineWidthFrac);
  
    // 4. Get down to business and do the work...	
  }

}