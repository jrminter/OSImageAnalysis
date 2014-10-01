# makeTilesMap_.py
#
# Process map images to a series of tiles for subsequent stitching.
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-01  JRM 0.1.00  This version has multiple base dir options

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

gitDir  = os.environ['GIT_HOME']
edsDir  = os.environ['EDS_ROOT']
relMap  = "/OSImageAnalysis/images/map"
# rptDir  = os.environ['RPT_ROOT']
basDir = gitDir
relInImg   = relMap + "/png"
relOutImg  = relMap + "/tile"

inExt     = ".png"
outExt    = ".tif"
lNames  = ["2-OK","3-CuL","4-PK","5-PdL","6-AgL","7-ROI"]

# No crop this time
# x  = 300
# y  = 50
# wd = 400
# ht = 500
# cropPar = [x,y,wd,ht]

inpDir = basDir + relInImg
outDir = basDir + relOutImg
# makeTiles(inpDir, outDir, lNames, inExt='.png', cropPar=None, bDebug=False):
jmg.makeTiles(inpDir, outDir, lNames) # , cropPar=cropPar)


