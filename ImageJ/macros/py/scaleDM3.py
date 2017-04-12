# scaleDM3.py
#
# Set the display limits for the current image plus
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-10-26  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
import csv
from ij.io import FileSaver

barW = 20
bCol = "White"
 
imp = IJ.getImage()
iW = imp.getWidth() 
iH = imp.getHeight()
ti = imp.getShortTitle()

IJ.run(imp, "Enhance Contrast", "saturated=0.35");
s2 = "x=0.5 y=0.5 width=%g height=%g interpolation=Bilinear average create title=%s" % (iW/2, iH/2, ti)
IJ.run(imp, "Scale...",s2 )

red = IJ.getImage()
IJ.run(red, "RGB Color","")
s2 = "width=%g height=6 font=24 color=%s location=[Lower Right] bold" % (barW, bCol)
IJ.run(red, "Add Scale Bar", s2)
red.show()

