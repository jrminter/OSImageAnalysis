# testCrop_.py
#
# Test cropping an image from an Oxford EDS map
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-15  JRM 0.1.00  initial prototype development.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
from io.scif.img import ImgOpener

edsDir  = os.environ['EDS_ROOT']
rptDir  = os.environ['RPT_ROOT']
relInImg  = "/testMap/png"
relOutImg  = "/testMap/tile"
inExt     = ".png"
outExt    = ".tif"
lInNames  = ["1-OK", "2-CuL", "3-PK", "4-PdL", "5-AgL", "6-line"]
x  = 300
y  = 50
wd = 400
ht = 500

cropPar = [x,y,wd,ht]

def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)

def doCrop(theImp, lPar):
  theImp.show()
  IJ.makeRectangle(lPar[0], lPar[1], lPar[2], lPar[3])
  IJ.run("Crop")
  imp = WindowManager.getCurrentImage()
  return (imp)

l = len(lInNames)
for i in range(l):
  print(lInNames[i])
  imgDir = edsDir + relInImg
  inImg = imgDir + "/" + lInNames[i] + inExt
  print(inImg)
  raw = IJ.openImage(inImg)
  raw.show()
  cr = doCrop(raw, cropPar)
  cr.show()
  imgDir = edsDir + relOutImg
  ensureDir(imgDir)
  outImg = "%s/tile-%g%s" % (imgDir, i+1, outExt)
  print(outImg)
  IJ.saveAsTiff(cr, outImg)
  cr.close()
  

