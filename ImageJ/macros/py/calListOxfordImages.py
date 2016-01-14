# calListOxfordImages.py
#
# Calibrate Oxford AZtec image files from image J and write with
# metadata
#
# This version uses lists of paramaters for a given sample and assumes
# the image file names are composed of a base name and a suffix
# followed by a file extension
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-01-14  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
from ij import IJ
from ij.io import DirectoryChooser, FileSaver
import jmFijiGen as jmg

bConvertNmToUm = True
sUser = "J. R. Minter"
sMicroscope = "FEI Sirion D5557"

mu = IJ.micronSymbol
sUnits	= mu + "m"

sBaseName = "qm-04592-KL-MF-121A-1-"

print(sUnits)

lImSuf = [            "02",  "03", "04", "05", "06", "07", "08", "09", 
          "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
          "20", "21", "22"] 
# lkV    = [ 15.,   15.,  15.,   15., 15.  ]
#           0    1    2    3   4     5    6    7    8     9
lMag   = [          15., 15., 10., 10., 10., 10., 10.,  10.,
           10.,  5.,  5.,  5.,  5.,  5.,  5.,  5.,  5.,   5.,      
            5.,  5., 10.]
# lFWu   = [ 44.5,  19.3, 44.5, 28.9, 57.9 ]

lkV = []
for i in range(len(lImSuf)):
	lkV.append(5.0)

lFWu = []
for i in range(len(lMag)):
	if (lMag[i] == 5.):
		lFWu.append(57.9)
	if (lMag[i] == 10.):
		lFWu.append(28.9)
	if (lMag[i] == 15.):
		lFWu.append(19.3)

print(lFWu)

lScan = []
for i in range(len(lMag)):
	if i < 5:
		lScan.append('20x1us')
	else:
		lScan.append('10x5us')
	


# dc = DirectoryChooser("Choose directory")
# basePath = dc.getDirectory()


basePath = "C:\\Data\\eds\\Oxford\\QM16-01-02A1-Nair\\reports\\qm-04592-KL-MF-121A-1\\tif\\"
calibDir = basePath + "calib\\"

print(basePath)

jmg.ensureDir(calibDir)

for i in range(len(lImSuf)):
	strPath = basePath + sBaseName + lImSuf[i] + ".tif"
	imp = IJ.openImage(strPath)
	imp.show()
	name = imp.getShortTitle()
	cal = imp.getCalibration()
	cal.setXUnit(sUnits)
	cal.setYUnit(sUnits)
	w = imp.getWidth()
	fScaleX = lFWu[i] / w
	cal.pixelWidth = fScaleX
	cal.pixelHeight = fScaleX
	sComment = "%g kV, S4, 5 mm, UHR TLD, tilt 0 deg, scan %s" % (lkV[i], lScan[i])
	newInfo = "Microscope: " + sMicroscope + " Software: Oxford AZtec 3.0, User: " + sUser +  "\n" + sComment
	imp.setProperty("Info", newInfo)
	imp.updateAndRepaintWindow()
	imp.setTitle(name)
	imp.show()
	time.sleep(1)

	imp.changes = False
	fs = FileSaver(imp)
	strPath = calibDir + name + ".tif"
	# let's make it platform agnostic
	if fs.saveAsTiff(strPath):
		msg = "Tif saved successfully at " + strPath
		print(msg) 
	imp.close()
	

print('done')
