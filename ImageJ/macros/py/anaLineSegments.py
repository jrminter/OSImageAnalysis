# anaLineSegments.py
#
# A reproducible example of analyzing particles after a watershed transform
# and drawing the features into the original image window. This uses helper
# functions to draw the ROI
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-01-28  JRM 0.1.00  Initial test on blob image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from java.awt import Color
from ij import IJ
from ij import ImagePlus
from ij.gui import Overlay, PointRoi, Roi
from ij.measure import ResultsTable, Measurements

def addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.white):
	"""addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.white)
	A convenience function to draw a ROI into the overlay of an ImagePlus. This is useful for
	situations where ROIs are computed from a highly processed image and the analyst wants to
	draw them into the overlay of the original image (e.g. particle analysis after a 
	watershed separation. Adapted from addToOverlay() from Analyzer.java

	Inputs:

	imp		- the ImagePlus instance into which we draw the ROI
	roi		- the ROI to draw
	labCol - the color or the label (default white)
	linCol - the color of the stroke/line (default white)

	Returns
	
	imp		- the ImagePlus with the updated overlay"""
	roi.setIgnoreClipRect(True)
	ovl = imp.getOverlay()
	if ovl == None:
		ovl = Overlay()
	ovl.drawNames(True)
	ovl.setStrokeColor(linCol)
	ovl.setLabelColor(labCol)
	ovl.drawBackgrounds(False)
	ovl.add(roi)
	imp.setOverlay(ovl)
	imp.updateImage()
	imp.updateAndRepaintWindow()
	return imp

def getLineLength(imp):
	x1=-1
	y1=-1
	x2=-1
	y2=-1
	roi = imp.getRoi()
	if roi != None:
		if roi.getType() == Roi.LINE:
			cal = imp.getCalibration()
			pw = cal.pixelWidth
			ph = cal.pixelHeight
			x1=roi.x1d
			y1=roi.y1d
			x2=roi.x2d
			y2=roi.y2d
			x = (x2-x1)*pw
			y = (y2-y1)*ph
			l = sqrt(x*x+y*y)
			imp = addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.green)
			# imp.updateAndRepaintWindow()			
			IJ.makePoint(-1,-1)
			# imp.updateAndRepaintWindow()
			return l, cal.getUnit()
	return None
IJ.run("Set Measurements...", "display redirect=None decimal=3")
IJ.run("Colors...", "foreground=black background=black selection=green")	
imp = IJ.getImage()
imp.updateAndRepaintWindow()
foo = getLineLength(imp)
imp.updateAndRepaintWindow()


print(foo)




