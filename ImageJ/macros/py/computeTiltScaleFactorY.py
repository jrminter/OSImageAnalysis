#  computeTiltScaleFactorY.py

#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-21  JRM 0.1.00  Initial prototype. 

import math

def computeTiltScaleFactorY(fScaleX, tiltDeg):
	"""computeTiltScaleFactorY(fScaleX, tiltDeg)
	Compute the fore-shortened Y-axis scale factor given the X-axis scale factor and tilt angle [deg]"""
	factor = math.cos(tiltDeg*math.pi/180.0) # convert to radians and compute cos
	fScaleY = fScaleX/factor
	return fScaleY
	print(fScaleX, fScaleY)

scaleX  = 4.45/1024. # 65kX AZtec 1025	
tiltDeg = 90.0 - 54.0

scaleY = computeTiltScaleFactorY(scaleX, tiltDeg)

print(scaleX, scaleY)