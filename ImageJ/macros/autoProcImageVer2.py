# @File file
# @double(label = "fwMicrons", value = 1.23) fwMicrons
# @double(label = "barWid", value=0.1) barWid
# @int(label = "barHt", value=6) barHt
# @int(label = "barFnt", value=24) barFnt
# @String(label = "barCol", value="Black") barCol
# @String(label = "barLoc", value="Lower Right") barLoc


# autoProcImageVer2.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-10-13  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ, Prefs
from ij.io import FileSaver 
import jmFijiGen as jmg
from ij.measure import Calibration

IJ.open(file.getAbsolutePath())
# load the dataset
imp = IJ.getImage()
fName = imp.getShortTitle()
wid = imp.getWidth()
argThree = "distance=%g known=%f pixel=1 unit=um" % (wid, fwMicrons)
IJ.run(imp, "Set Scale...", argThree)
IJ.run(imp, "Enhance Contrast", "saturated=0.35")
fPath = file.getParent()
fPath.replace("\\", "/")
tifName = fName + ".tif"
tifPath = os.path.join(fPath, tifName)


print(fName)
imp.changes = False
wid = imp.getWidth()
mu = IJ.micronSymbol
scaUni	= mu + "m"
argThree = "distance=%g known=%f pixel=1 unit=%s" % (wid, fwMicrons, scaUni)
IJ.run(imp, "Set Scale...", argThree)
IJ.run(imp, "Enhance Contrast", "saturated=0.35")

fs = FileSaver(imp)
print(tifPath)
if fs.saveAsTiff(tifPath):
	print "Tif saved successfully at ", tifPath  

IJ.run(imp, "RGB Color", "")
# dummy to get things set
foo = imp.duplicate()
s2 = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barWid, barHt, barFnt, barCol, barLoc)
IJ.run(foo, "Add Scale Bar", s2)
# explicitly save preferences
Prefs.savePreferences()
foo.changes = False
foo.close()
IJ.run(imp, "Add Scale Bar", s2)
imp.setTitle(fName)
fs = FileSaver(imp) 
pngName = fName + ".png"
pngPath = os.path.join(fPath, pngName)
if fs.saveAsPng(pngPath):
	print "png saved successfully at ", pngPath  


