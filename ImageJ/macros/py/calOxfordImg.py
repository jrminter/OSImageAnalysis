# calOxfordImg.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-29  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ
import jmFijiGen as jmg

fwUnits = 2.89
units = IJ.micronSymbol + "m"

imp = IJ.getImage()
imp = jmg.calibImage(imp, fwUnits, units=-6)
