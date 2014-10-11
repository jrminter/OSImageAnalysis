# stitchTiles_.py
#
# Stitch Oxford EDS maps and burn scale bars
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-18  JRM 0.1.00  For tiles from paint cross-section

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
import jmFijiGen as jmg

edsDir  = os.environ['EDS_ROOT']
# rptDir  = os.environ['RPT_ROOT']
relImg  = "/Oxford/Paint-Cross-Section/reports/map1/tile"
relOut  = "/Oxford/Paint-Cross-Section/reports/map1"
outNam = "Paint-Cross-Section-20kV-m01-4x3.png"

imgDir = edsDir + relImg

print(imgDir)

# 2X3
# x      = 2
# y      = 3
# 3X2
x      = 4
y      = 3
scale  = 0.2578
units  = "um"
pts    = 32
barCol = "White"

myImp = jmg.stitchMaps(imgDir, x, y)
myImp.show()
jmg.addScaleBar(myImp, scale, units, 10, 10, pts, barCol, "Lower Right")


# Get the final map 
imp = WindowManager.getCurrentImage()

outDir = edsDir + relOut
jmg.ensureDir(outDir)
outPth = outDir + "/" + outNam
print(outPth)
IJ.saveAs(imp, "PNG", outPth)

