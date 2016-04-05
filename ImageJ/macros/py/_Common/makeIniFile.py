# @File file
# @boolean(label = "append") bAppend
# @boolean(label = "FIB") bFIB
# @double(label = "imgWid", value=1024) imgWid
# @int(label = "kV", value=5) iKV
# @int(label = "spot", value=3) iSpot
# @double(label = "working distance", value = 5.0) dFWD
# @double(label = "tilt Angle", value = 0) dTiltDeg
# @String(label = "detector", value="UHR TLD") sDetector
# @String(label = "scan", value="1X10us") sScan
# @String(label = "Other Comment", value="Lower Right") sOtherComment
# @String(label = "baseName", value="qm-01234-sample") baseName
# @double(label = "mag (X)", value = 1) magX

# makeAZtecIni.py
# A script to write metadata for an AZtec image to an ini file
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-02-02  JRM 0.1.00  Initial prototype - a work in progress
# 2016-04-05  JRM 0.1.10  Compute scale from inverse mag plot linear model
#                         Also re-arranged dialog to minimize moves
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

def estimateAztecScaleFactorX(mag, scanWidthPx=1024, slope=289251.80, slopeSE=16.54, rDigits=7):
	"""estimateAztecScaleFactorX(mag, scanWidthPx=1024, slope=289251.80, slopeSE=16.54
	
	Estimate the scale factor [microns/px] from a linear fit of the image full width
	as a function of the inverse magnification.

	Parameters
    ----------
    mag: number
        The SEM magnification
    scanWidthPx: number (1024)
    	The full width of the image scan in pixels. The maximum is 4096
    slope: number (289251.80)
    	The slope of the inverse magnification plot. Note the intercept is constrained
    	to zero.
    slopeSE: number (16.54)
    	The standard error of the fit.  
    rDigits: integer (5)
    	Number of digits to round the microns/pix

    Returns
    -------
    sf: list [mean, LCL, UCL]
    	The scale factor in microns per pixel. The first value is the mean.
    	The second and third values are the lower and upper confidence intervals.
	"""
	imFWMu  = slope/mag
	imFWLCL = (slope-slopeSE)/mag
	imFWUCL = (slope+slopeSE)/mag
	sfMu = round(imFWMu/scanWidthPx, rDigits)
	sfLC = round(imFWLCL/scanWidthPx, rDigits)
	sfUC = round(imFWUCL/scanWidthPx, rDigits)
	sf = [sfMu, sfLC, sfUC]
	return sf

# print(dir(file))
print(file.path)

if bAppend:
	f = open(file.path, 'a')
else:
	f = open(file.path, 'w')
f.write("[" + baseName + "]\n")
strLine = "Mag=%.1f" %  magX + "\n"
f.write(strLine)
# fScaleX = fwMicrons/imgWid
fScale = estimateAztecScaleFactorX(magX, scanWidthPx=imgWid, slope=289251.80, slopeSE=16.54, rDigits=7)
fScaleX = fScale[0]
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


