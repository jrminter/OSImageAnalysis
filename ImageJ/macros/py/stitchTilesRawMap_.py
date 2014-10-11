# stitchTilesrawMap_.py
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
relImg  = "/Oxford/qm-04080-15kV-KS2013-12-12-19-top-line-map/reports/raw-map/tile"
relOut  = "/Oxford/qm-04080-15kV-KS2013-12-12-19-top-line-map/reports/raw-map"
outNam = "qm-04080-15kV-KS2013-12-12-19-top-line-raw-map-7kV-3x3.png"

imgDir = edsDir + relImg

print(imgDir)

# 2X3
# x      = 2
# y      = 3
# 3X2
x      = 3
y      = 3
scale  = 0.1445
a = [0xCE, 0xBC]
mu = "".join([chr(c) for c in a]).decode('UTF-8')
units  = mu+"m"
pts    = 18
barCol = "White"

myImp = jmg.stitchMaps(imgDir, x, y)
myImp.show()
#                                  scale sz
jmg.addScaleBar(myImp, scale, units, 5,  5, pts, barCol, "Lower Right")


# Get the final map 
imp = WindowManager.getCurrentImage()

outDir = edsDir + relOut
jmg.ensureDir(outDir)
outPth = outDir + "/" + outNam
print(outPth)
IJ.saveAs(imp, "PNG", outPth)

