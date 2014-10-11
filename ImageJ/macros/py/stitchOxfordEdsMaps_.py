# stitchOxfordEdsMaps_.py
#
# Stitch Oxford EDS maps and burn scale bars
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-11  JRM 0.1.00  initial prototype development.
# 2014-09-15  JRM 0.1.10  added cropping and saving output
# 2014-09-17  JRM 0.1.15  Import functions from jmFijiGen.py

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
rptDir  = os.environ['RPT_ROOT']
# for uncropped images
# relImg  = "/testMap/png/ij"
# for cropped images
relImg  = "/testMap/tile"
relOut  = "/testMap/out"
outNam = "445005-248-Pd8-1-FIB-7kV-m01-3x2.png"

imgDir = edsDir + relImg

print(imgDir)

# 2X3
# x      = 2
# y      = 3
# 3X2
x      = 3
y      = 2
scale  = 2.822
units  = "nm"
pts    = 32
barCol = "Black"

myImp = jmg.stitchMaps(imgDir, x, y)
myImp.show()

jmg.addScaleBar(myImp, scale, units, 100, 9, pts, barCol, "Lower Right")


# Get the final map 
imp = WindowManager.getCurrentImage()
outDir = edsDir + relOut
jmg.ensureDir(outDir)
outPth = outDir + "/" + outNam
print(outPth)
IJ.saveAs(imp, "PNG", outPth)
