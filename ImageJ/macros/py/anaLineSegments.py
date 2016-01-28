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
import jmFijiGen as jmg

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
			jmg.addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.green)
			# imp.updateAndRepaintWindow()			
			IJ.makePoint(-1,-1)
			imp.updateAndRepaintWindow()
			return l, cal.getUnit()
	return None

	
imp = IJ.getImage()
foo = getLineLength(imp)
imp.updateAndRepaintWindow()

print(foo)




