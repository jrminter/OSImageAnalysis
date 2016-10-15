# @File file
# @boolean(label = "append") append
# @boolean(label = "FIB") fib
# @String(label = "Image Width", value="1024") imgwidth
# @String(label = "kV", value="5.0") kv
# @String(label = "spot", value="3") spot
# @String(label = "working distance", value="5.0") fwd
# @String(label = "tilt Angle [deg]", value="0.0") tilt
# @String(label = "detector", value="UHR TLD") det
# @String(label = "scan", value="1X10us") scan
# @String(label = "Other Comment", value="Lower Right") comment
# @String(label = "base image name", value="qm-01234-sample") basename
# @String(label = "mag (X)", value="1.0") mag

# makeAZtecIni.py
# A script to write metadata for an AZtec image to an ini file
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-02-02  JRM 0.1.00  Initial prototype - a work in progress
# 2016-04-05  JRM 0.1.10  Compute scale from inverse mag plot linear model
#                         Also re-arranged dialog to minimize moves
# 2016-04-06  JRM 0.1.15  Print better diagnostics
# 2016-09-27  JRM 0.1.16  Latest scijava seems to not like integers and doubles
# 2016-10-14  JRM 0.1.17  Finally get rid of the ints...
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
# print(file.path)

imgwidth = int(imgwidth)
kv = float(kv)
spot = int(spot)
fwd = float(fwd)
tilt = float(tilt)
mag = round(float(mag), 1)

if append:
	f = open(file.path, 'a')
else:
	f = open(file.path, 'w')
f.write("[" + basename + "]\n")
strLine = "Mag=%.1f" %  mag + "\n"
f.write(strLine)
# fScaleX = fwMicrons/imgwidth
fScale = estimateAztecScaleFactorX(mag, imgwidth, slope=289251.80, slopeSE=16.54, rDigits=7)
fScaleX = fScale[0]
strLine = "ScaleX=%.6f" %  fScaleX + "\n"
f.write(strLine)
if fib:
	tiltDeg = 90.0 - tilt
else:
	tiltDeg = tilt

fScaleY = computeTiltScaleFactorY(fScaleX, tiltDeg)
strLine = "ScaleY=%.6f" %  fScaleY + "\n"
f.write(strLine)
strLine = "Units=µm\n"
f.write(strLine)
strLine = "Comment=%g kV, S%d, %.1f mm, %s, %.1f deg tilt, %s, %s\n\n" % (kv, spot, fwd, det, tilt, scan, comment )
f.write(strLine)

f.close()

strMsg = "Processed image %s at magnification %.1fX" % (basename, mag)
print(strMsg)

