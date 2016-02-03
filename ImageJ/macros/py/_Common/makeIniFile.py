# @File file
# @boolean(label = "append") bAppend
# @boolean(label = "FIB") bFIB
# @double(label = "imgWid", value=1024) imgWid
# @String(label = "baseName", value="qm-01234-sample") baseName
# @int(label = "kV", value=5) iKV
# @int(label = "spot", value=3) iSpot
# @double(label = "working distance", value = 5.0) dFWD
# @double(label = "tilt Angle", value = 0) dTiltDeg
# @double(label = "mag (X)", value = 1) magX
# @double(label = "fwMicrons", value = 1.23) fwMicrons
# @String(label = "detector", value="UHR TLD") sDetector
# @String(label = "scan", value="1X10us") sScan
# @String(label = "Other Comment", value="Lower Right") sOtherComment

# makeAZtecIni.py
# A script to write metadata for an AZtec image to an ini file
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-02-02  JRM 0.1.00  Initial prototype - a work in progress
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os, math
from ij import IJ, Prefs
from ij.io import FileSaver 
import jmFijiGen as jmg
from ij.measure import Calibration

def computeTiltScaleFactorY(fScaleX, tiltDeg):
	"""computeTiltScaleFactorY(fScaleX, tiltDeg)
	Compute the fore-shortened Y-axis scale factor given the X-axis scale factor and tilt angle [deg]"""
	factor = math.cos(tiltDeg*math.pi/180.0) # convert to radians and compute cos
	fScaleY = fScaleX/factor
	return fScaleY

print(dir(file))
print(file.path)

if bAppend:
	f = open(file.path, 'a')
else:
	f = open(file.path, 'w')
f.write("[" + baseName + "]\n")
strLine = "Mag=%.1f" %  magX + "\n"
f.write(strLine)
fScaleX = fwMicrons/imgWid
strLine = "ScaleX=%.6f" %  fScaleX + "\n"
f.write(strLine)
if bFIB:
	tiltDeg = 90.0 - dTiltDeg
else:
	tiltDeg = dTiltDeg

fScaleY = computeTiltScaleFactorY(fScaleX, tiltDeg)
strLine = "ScaleY=%.6f" %  fScaleY + "\n"
f.write(strLine)
strLine = "Units=µm\n"
f.write(strLine)
strLine = "Comment=%d kV, S%d, %.1f mm, %s, %.1f deg tilt, %s, %s\n\n" % (iKV, iSpot, dFWD, sDetector, dTiltDeg, sScan, sOtherComment )
f.write(strLine)

f.close()


