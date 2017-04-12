from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
setSpecificDisplayLimits.py

Set the display limits for the active image plus

Modifications

  Date      Who  Ver                      What
----------  --- ------  ------------------------------------------------
2015-12-15  JRM 0.1.00  Initial prototype
2017-04-12  JRM 0.1.10  PEP8 and move codecs to top
"""

gLo                =  2000.
gHi                = 20000.
bSetScaleFromWidth = True
imgWidth           = 5.79
strUnits           = "um"

# Should not need to change below here...

import os
import time
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
import csv
from ij.io import FileSaver



imp = IJ.getImage()
iWid = imp.getWidth() 

if bSetScaleFromWidth:
    sArg3 =  "distance=%d known=%f pixel=1 unit=%s" % (iWid, imgWidth, strUnits) 
    IJ.run(imp, "Set Scale...", sArg3)

ip = imp.getProcessor()
ip.setMinAndMax(gLo, gHi)
imp.updateImage()
imp.setDisplayRange(gLo, gHi)
imp.updateAndRepaintWindow()


luts = imp.getLuts()
print(luts)
