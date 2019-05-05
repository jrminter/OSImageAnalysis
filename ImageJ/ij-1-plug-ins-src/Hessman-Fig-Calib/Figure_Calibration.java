// Figure_Calibration.java
// Author: Frederic V. Hessman (hessman at Astro.physik.Uni-Goettingen.de)
// source: http://www.astro.physik.uni-goettingen.de/~hessman/ImageJ/Figure_Calibration/

import java.awt.*;

import ij.*;
import ij.gui.*;
import ij.measure.*;
import ij.plugin.filter.*;
import ij.process.*;

public class Figure_Calibration implements PlugInFilter
	{
	ImagePlus img;

	public int setup(String arg, ImagePlus imp)
		{
		img = imp;
		return DOES_ALL;
		}

	public void run(ImageProcessor ip)
		{
		Roi roi = img.getRoi();
		if (roi == null)
			{
			IJ.error("No ROI to define coordinate system!");
			return;
			}
		Rectangle rect = roi.getBounds();

		double x1=0.0, x2=1.0, y1=0.0, y2=1.0;

		GenericDialog gd = new GenericDialog ("Figure Calibration");
		gd.addMessage("Input figure values:");
		gd.addNumericField("x(lower-left)",x1,2);
		gd.addNumericField("x(upper-right)",x2,2);
		gd.addNumericField("y(lower-left)",y1,2);
		gd.addNumericField("y(upper-right)",y2,2);
		gd.showDialog();
		if (gd.wasCanceled()) return;
		x1 = gd.getNextNumber();
		x2 = gd.getNextNumber();
		y1 = gd.getNextNumber();
		y2 = gd.getNextNumber();

		// xcal = pixelWidth*(i-xOrigin)
		// ycal = pixelHeight*(j-yOrigin)

		Calibration cal = img.getLocalCalibration();
		cal.pixelWidth =  (x2-x1)/rect.width;
		cal.pixelHeight = (y1-y2)/rect.height;
		cal.xOrigin = rect.x-(x1/cal.pixelWidth);
		cal.yOrigin = rect.y-(y2/cal.pixelHeight);
		}
	}
