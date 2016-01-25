#  computeTiltScaleFactorY.py

#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-21  JRM 0.1.00  Initial prototype. 

import math
from ij import IJ

def computeTiltScaleFactorY(fScaleX, tiltDeg):
	"""computeTiltScaleFactorY(fScaleX, tiltDeg)
	Compute the fore-shortened Y-axis scale factor given the X-axis scale factor and tilt angle [deg]"""
	factor = math.cos(tiltDeg*math.pi/180.0) # convert to radians and compute cos
	fScaleY = fScaleX/factor
	return fScaleY
	print(fScaleX, fScaleY)


mu = IJ.micronSymbol

stageTilt = 52.0

scaUni	= mu + "m"
mag = "80K"
scaleX  = 3.62 /1024. # 65kX AZtec 4.45/1024	
tiltDeg = 90.0 - stageTilt

scaleY = computeTiltScaleFactorY(scaleX, tiltDeg)
strMsg = "Stage Tilt: %.1f, Foreshortening Tilt: %.1f deg, Mag = %s, ScaleX: %.7f, ScaleY: %.7f %s"     % (stageTilt, tiltDeg, mag, scaleX, scaleY, scaUni)
print(strMsg)