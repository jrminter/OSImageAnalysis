# procSemIni.py
#
# Read a .ini file written by the Imaging C Module 'WriteImageInfoFolder'
# reading the image name, magnification, X- and Y-axis scales and unit string.
# If the unit string is in nm, it converts to microns. It opens the image,
# calibrates the scale and saves the image.
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-11  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
import csv
from ij.io import FileSaver
import ConfigParser

bConvertNmToUm = True
sUser = "J. R. Minter"
sMicroscope = "FEI Sirion D5557"
basePath = '/Users/jrminter/dat/images/test/qm-04570-1421DJD-04-C03/'
iniPath = basePath + 'ImageMetadata.ini'
os.chdir(basePath)
mu = IJ.micronSymbol

calibDir = basePath + "calib/"
jmg.ensureDir(calibDir)



config = ConfigParser.RawConfigParser()
config.read(iniPath)

# get a list of the images
sect = config.sections()

print(len(sect))
print(sect[0])

for imgName in sect:
	fMag     = config.getfloat(imgName, "Mag")
	fScaleX  = config.getfloat(imgName, "ScaleX")
	fScaleY  = config.getfloat(imgName, "ScaleY")
	sUnits   = config.get(imgName, "Units")
	if (bConvertNmToUm == True):
		if(sUnits == "nm"):
			fScaleX /= 1000.
			fScaleY /= 1000.
			sUnits =  mu + "m"
	sComment = config.get(imgName, "Comment")
	strPath = basePath + imgName + ".tif"
	imp = IJ.openImage(strPath)
	cal = imp.getCalibration()
	cal.setXUnit(sUnits)
	cal.setYUnit(sUnits)
	cal.pixelWidth = fScaleX
	cal.pixelHeight = fScaleY
	obinfo = imp.getProperty("Info")
	newInfo = "Microscope: " + sMicroscope + " Software: analySIS 5.0, User: " + sUser +  "\n" + sComment
	imp.setProperty("Info", newInfo)
	imp.show()
	time.sleep(1)

	imp.changes = False
	fs = FileSaver(imp)
	strPath = calibDir + imgName + ".tif"
	if fs.saveAsTiff(strPath):
		print "Tif saved successfully at ", strPath
	imp.close()


print("done")



