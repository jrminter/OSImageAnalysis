# writeBareOxfordMetadataIni.py
#
# Write a bare metadata file to use to calibrate Oxford AZtec image files
# This version uses the BF&I approach to write the .ini file to get
# the order right... We can edit this to add specific data for individual images
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-01-25  JRM 0.1.00  Initial prototype for qm-04599-LMF-695P

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import math
from ij.io import DirectoryChooser

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()

iniPath = basePath + os.sep + 'ImageMetadata.ini'

baseImg = "qm-04599-LMF-695P-FIB"

lImgNo = range(1,13,1)

def computeTiltScaleFactorY(fScaleX, tiltDeg):
	"""computeTiltScaleFactorY(fScaleX, tiltDeg)
	Compute the fore-shortened Y-axis scale factor given the X-axis scale factor and tilt angle [deg]"""
	factor = math.cos(tiltDeg*math.pi/180.0) # convert to radians and compute cos
	fScaleY = fScaleX/factor
	return fScaleY

def calcMag(imgNo):
	if imgNo <= 4:
		fMag = 250000.
	else:
		fMag = 150000.
	return fMag

def calcFW(imgNo):
	if imgNo <= 4:
		fFW = 1.16
	else:
		fFW = 1.93
	return fFW

def scanTime(imgNo):
	if imgNo <= 10:
		sScanT = '1x15us'
	else:
		sScanT = '1x75us'
	return sScanT


e0 = 15
stgTilt  = 52.0

sUnit    = "µm"


names = []

for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

# open the ini file
f=open(iniPath, 'w')

i = 0

for name in names:
	i +=1
	print(name)
	strLine = "[" + name + "]"
	f.write(strLine +'\n')
	fMag = calcMag(i)
	fW = calcFW(i)
	scan = scanTime(i)
	fScaleX = fW / 1024.
	fScaleY = computeTiltScaleFactorY(fScaleX, stgTilt)
	sComment = "%d kV, S4, 5 mm, UHR TLD SE+BSE, tilt %.0f deg, %s" % (e0, stgTilt, scan)
	strLine = "Mag = %.1f" % fMag
	f.write(strLine +'\n')
	strLine = "ScaleX = %.6f" % fScaleX
	f.write(strLine +'\n')
	strLine = "ScaleY = %.6f" % fScaleY
	f.write(strLine +'\n')
	strLine = "Units = %s" % sUnit
	f.write(strLine +'\n')
	strLine = "Comment = %s" % sComment
	f.write(strLine +'\n')
	# write a space between sections
	f.write('\n')

f.close()

print('done')
