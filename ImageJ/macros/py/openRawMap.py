# openRawMap.py
#
# J. R. Minter
# CCA licence
#
# Open a raw EDS map exported from the AZtec softeware as as an IMAGE cube
# w/o using the GUI. One would need to switch indicies and do the transformation
# described by Zach Gainford in his Bruker example from Microscopy Today Sep 2014 pg75.
# which uses a VECTOR cube.
#
# Note: this was adapted from Albert Cardona's example of how to implement a new file format reader
# http://albert.rierol.net/imagej_programming_tutorials.html#How to integrate a new file format reader and writer
#
#
#  date       who  comment
# ----------  ---  -----------------------------------------------------
# 2015-10-10  JRM  initial prototype
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, ImagePlus, ImageStack
from ij.io import FileInfo, FileOpener
from ij.measure import Calibration

imgDir = "D:/Data/eds/hyperspy/qm-04355-Paint-xs-20kV-map1/"
imgNam = "qm-04355-Paint-xs-20kV-map1.raw"

def openRplRawImageCube(fDir, fName, width, height, nChan, umPerPx=0.5156, evPerCh=10.0, evOff=-100.0):
	fi = FileInfo()
	# fi.fileType = fi.GRAY16_SIGNED
	fi.fileType = fi.GRAY16_UNSIGNED
	fi.fileFormat = fi.RAW
	fi.directory = fDir
	fi.fileName  = fName
	fi.width = width
	fi.height = height
	fi.nImages = nChan
	fi.gapBetweenImages = 0
	fi.intelByteOrder = True      # little endian
	fi.whiteIsZero = False        # no inverted LUT
	fi.longOffset = fi.offset = 0 # header size, in bytes
	fo = FileOpener(fi)
	imp = fo.open(False)
	cal = Calibration()
	cal.xOrigin = 0.
	cal.yOrigin = 0.
	cal.zOrigin = evOff/evPerCh
	cal.pixelWidth = umPerPx
	cal.pixelHeight = umPerPx
	cal.pixelDepth = evPerCh
	mu = IJ.micronSymbol
	scaUni	= mu + "m"
	cal.setXUnit(scaUni)
	cal.setYUnit(scaUni)
	cal.setZUnit("eV")
	tImp = ImagePlus()
	tImp.setStack(imp.getTitle(), imp.getStack())
	tImp.setCalibration(cal)
	IJ.run(tImp, "32-bit", "")
	stack = tImp.getImageStack()
	gMin = 32000.
	gMax = -32000.
	iMax = 0
	for i in xrange(1, tImp.getNSlices()+1):
		ip = stack.getProcessor(i)
		mV = ip.getMin()
		if (mV < gMin):
			gMin = mV
		mV = ip.getMax()
		if (mV > gMax):
			gMax = mV
			iMax = i
	IJ.setMinAndMax(tImp, gMin, gMax)
	# set to the channel with max intensity
	tImp.setPosition(iMax)
	print("Max intensity %.2f at channel %g" % (gMax, iMax ))
	return tImp


orig = openRplRawImageCube(imgDir, imgNam, 256, 192, 2048)
orig.show()








