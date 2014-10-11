# testCrop_.py
#
# Test cropping an image from an Oxford EDS map
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-15  JRM 0.1.00  initial prototype development.
# 2014-09-17  JRM 0.1.01  uses jmFijiGen.py import of doCrop.

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
relInImg  = "/testMap/png"

inDir = edsDir + relInImg 
imgName = "6-line.png"

inImg = inDir + "/" + imgName

# x  = 300
# y  = 50
# wd = 400
# ht = 500

x  = 350
y  = 70
wd = 400
ht = 400

cropPar = [x,y,wd,ht]

raw = IJ.openImage(inImg)
raw.show()

cr = jmg.doCrop(raw, cropPar)
cr.show()
