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

imgDir  = os.environ['IMG_ROOT']
edsDir  = os.environ['EDS_ROOT']
# relInImg  = "/QM15-02-03A-Nair/qm-04249-MIS-12-105-cryo/png"
relInImg  = "/Oxford/QM15-04-01B-Steele/reports/qm-04261-44T005-294-Cu-blue/qm-04261-44T005-294-Cu-blue-7kV-map2/msa"

# inDir = imgDir + relInImg 
inDir = edsDir + relInImg 
# imgName = "qm-04249-MIS-12-105-cryo-15-s3.png"
imgName = "ppts.png"

inImg = inDir + "/" + imgName

print(inImg)

# 6-line.png
# x  = 300
# y  = 70
# wd = 400
# ht = 400

x  = 170
y  = 40
wd = 3670
ht = 1780

cropPar = [x,y,wd,ht]

raw = IJ.openImage(inImg)
raw.show()

cr = jmg.doCrop(raw, cropPar)
cr.show()
