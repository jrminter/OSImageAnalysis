# makeTiles_.py
#
# Process map images from paint cross-sections to a series of tiles
# for subsequent stitching.
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-18  JRM 0.1.00  Process map images from paint cross-sections

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
# rptDir  = os.environ['RPT_ROOT']
relInImg  = "/Oxford/Paint-Cross-Section/reports/map1/png"
relOutImg  = "/Oxford/Paint-Cross-Section/reports/map1/tile"
inExt     = ".png"
outExt    = ".tif"
lNames  = ["1-CaK","2-TiK","3-FeK","4-AlK","5-SK","6-BaL","7-PbM","8-SiK","9-MgK","10-OK","11-CK","12-ROI"]

# No crop this time
# x  = 300
# y  = 50
# wd = 400
# ht = 500
# cropPar = [x,y,wd,ht]

inpDir = edsDir + relInImg
outDir = edsDir + relOutImg
# makeTiles(inpDir, outDir, lNames, inExt='.png', cropPar=None, bDebug=False):
jmg.makeTiles(inpDir, outDir, lNames) # , cropPar=cropPar)


