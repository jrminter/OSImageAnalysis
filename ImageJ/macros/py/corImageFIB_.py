# corImageFIB_.py
#
# Correct the aspect ratio of a FIB image and calibrate it
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-06-25  JRM 0.1.00  Get'er done

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import math
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager

def corImageFIB(imp, umPerPx):
  """ corImageFIB(imp, umPerPx)
  Correct the aspect ratio of a FIB image stitched with analySIS 5.0.
  Note: FEI and SIS did/do some undocumented image manipulation under
  the hood. This was worked out using analySIS to stitch the base image
  and then correcting for their misdeeds. Their code reproducibly scales
  the height by a factor of 1.154135."""

  mu = IJ.micronSymbol
  scaUni  = mu + "m"

  ti = imp.getShortTitle() + "-arc"
  wd = imp.getWidth()
  ht = imp.getHeight()
  newHt = int(round(1.154135*ht,0))
  strArg = "x=- y=- width=%d height=%d interpolation=Bicubic average create title=%s" % (wd, newHt, ti)
  IJ.run("Scale...", strArg);
  strArg = "distance=1 known=%f pixel=1 unit=%s" % (umPerPx, scaUni)
  IJ.run("Set Scale...", strArg)
  print(newHt)


impWrk = WindowManager.getCurrentImage()
impWrk.show()

# jmg.corImageFIB(impWrk, 0.008783)
jmg.corImageFIB(impWrk, 0.01757)



