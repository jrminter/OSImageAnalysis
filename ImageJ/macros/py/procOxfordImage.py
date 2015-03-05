# procOxfordImage.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-24  JRM 0.1.00  initial prototype.
#
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os

from ij import IJ

units = IJ.micronSymbol + "m"
fieldWid =  82.7 # from details Oxford dialog 

# get the active image
ori = IJ.getImage()
IJ.run(ori, "Enhance Contrast", "saturated=0.35");
imgWid = ori.getWidth()
strScale = "distance=%g known=%g pixel=1 unit=%s" % (imgWid, fieldWid, units)
IJ.run(ori, "Set Scale...", strScale)




