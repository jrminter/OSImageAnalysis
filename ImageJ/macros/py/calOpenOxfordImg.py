# calOpenOxfordImg.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-29  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ
from ij.io import FileSaver
import jmFijiGen as jmg

fwUnits = 5.79

units = IJ.micronSymbol + "m"

imp = IJ.getImage()
imp = jmg.calibImage(imp, fwUnits, units=-6)
imp.updateAndRepaintWindow()

print("done")
