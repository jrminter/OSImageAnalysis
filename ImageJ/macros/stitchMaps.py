# stitchTilesMap_.py
#
# Stitch Oxford EDS maps and calibrate final image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-01  JRM 0.1.00  Stitch map exemplars. This version just
#                         calibrates the map so the scale bar can be more
#                         precisely placed and then the map may be annotated

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
import jmFijiGen as jmg


gitDir  = os.environ['GIT_HOME']
edsDir  = os.environ['EDS_ROOT']
relMap  = "/OSImageAnalysis/images/map"
# rptDir  = os.environ['RPT_ROOT']
# this exemplar in the GIT root tree
basDir = gitDir
relImg  = relMap + "/tile"
relOut  = relMap

outNam = "exemplar-3x2-map.png"

imgDir = basDir + relImg

print(imgDir)

# 2X3
# x      = 2
# y      = 3
# 3X2
x      = 3
y      = 2
scale  = 2.832
# Here is how one does a mu...
# a = [0xCE, 0xBC]
# mu = "".join([chr(c) for c in a]).decode('UTF-8')
# units  = mu+"m"
units = "nm"
pts    = 24
barCol = "White"

myImp = jmg.stitchMaps(imgDir, x, y)
myImp.show()
# in this case we want to add by hand so we can position to selection
#                                  scale  sz
# jmg.addScaleBar(myImp, scale, units, 100,  8, pts, barCol, "Lower Right")


# Get the final map 
imp = WindowManager.getCurrentImage()
strSca = "distance=1 known=%.3f unit=%s" % (scale, units)
IJ.run("Set Scale...", strSca)

outDir = basDir + relOut
jmg.ensureDir(outDir)
outPth = outDir + "/" + outNam
print(outPth)
IJ.saveAs(imp, "PNG", outPth)

