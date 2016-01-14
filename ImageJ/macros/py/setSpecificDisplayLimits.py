# setSpecificDisplayLimits.py
#
# Set the display limits for the current image plus
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-15  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
import csv
from ij.io import FileSaver

fLo    = 1800.
fHi    = 11000.
# fUmWid = 4.45 # microns

 
imp = IJ.getImage()
iWid = imp.getWidth() 

# sArg3 =  "distance=%d known=%f pixel=1 unit=um" % (iWid, fUmWid)
# IJ.run(imp, "Set Scale...", sArg3);
ip = imp.getProcessor()
ip.setMinAndMax(fLo, fHi)
imp.updateImage()
imp.setDisplayRange(fLo, fHi)
imp.updateAndRepaintWindow()


luts = imp.getLuts()
print(luts)
