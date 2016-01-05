# setMetaDataActiveImage.py
#
# set the metadata in the active image manually
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  ----------------------------------------------
# 2016-01-05  JRM 0.0.90  Initial prototype.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ

# change these as needed
sUser = "J. R. Minter"
sMicroscope = "FEI Sirion D5557"
sSoftware = "Oxford AZtec 3.0"
sComment = "7 kV, S4, 5 mm, UHR TLD SE+BSE, tilt 52 deg"
# can easily calc these from computeTiltScaleFactorY.py
fMag     =  65000.
fScaleX  = 0.004346
fScaleY  = 0.005515
sUnits =  IJ.micronSymbol + "m"
# sUnits   = "nm"

imp = IJ.getImage()
print(imp.getShortTitle())
cal = imp.getCalibration()
cal.setXUnit(sUnits)
cal.setYUnit(sUnits)
cal.pixelWidth = fScaleX
cal.pixelHeight = fScaleY
obinfo = imp.getProperty("Info")
newInfo = "Microscope: " + sMicroscope + " Software:" + sSoftware + ", User: " + sUser +  "\n" + sComment
imp.setProperty("Info", newInfo)
imp.updateAndRepaintWindow()