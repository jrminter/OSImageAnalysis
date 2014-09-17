# testCropSeries_.py
#
# Test cropping an image series from an Oxford EDS map to a series of tiles
# for subsequent stitching.
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-15  JRM 0.1.00  initial prototype development.
# 2014-09-17  JRM 0.1.01  uses jmFijiGen.py import of makeTiles

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
from io.scif.img import ImgOpener
import jmFijiGen as jmg

edsDir  = os.environ['EDS_ROOT']
rptDir  = os.environ['RPT_ROOT']
relInImg  = "/testMap/png"
relOutImg  = "/testMap/tile"
inExt     = ".png"
outExt    = ".tif"
lNames  = ["1-OK", "2-CuL", "3-PK", "4-PdL", "5-AgL", "6-line"]
x  = 300
y  = 50
wd = 400
ht = 500

cropPar = [x,y,wd,ht]
inpDir = edsDir + relInImg
outDir = edsDir + relOutImg
# makeTiles(inpDir, outDir, lNames, inExt='.png', cropPar=None, bDebug=False):
jmg.makeTiles(inpDir, outDir, lNames, cropPar=cropPar)


