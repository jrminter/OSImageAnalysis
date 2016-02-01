# procSirionSisIni.py
#
# Read a .ini file written by the the 'writeBareMetadataIni.py' script
# after editing for AnalySIS metadata
# reading the image name, magnification, X- and Y-axis scales and unit string.
# If the unit string is in nm, it converts to microns. It opens the image,
# calibrates the scale and saves the image.
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-16  JRM 0.1.00  Initial prototype. Now path separator agnostic
# 2015-12-17  JRM 0.1.10  Work from tif files to keep in order.
# 2016-02-01  JRM 0.1.20  Add magnification to comment in Info field. Rename.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ, Prefs, WindowManager
import csv
from ij.io import FileSaver, DirectoryChooser
import ConfigParser

bConvertNmToUm = True
sUser = "J. R. Minter"
sMicroscope = "FEI Sirion D5557"


lastPath = Prefs.get("Last.Image.Dir", "None")
if os.path.exists(lastPath):
	os.chdir(lastPath)

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()
Prefs.set("Last.Image.Dir", basePath)

names = []
for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

# basePath = '/Users/jrminter/dat/images/test/qm-04570-1421DJD-04-C03/'
iniPath = basePath + os.sep + 'ImageMetadata.ini'
os.chdir(basePath)
mu = IJ.micronSymbol
calibDir = basePath + "calib" + os.sep
jmg.ensureDir(calibDir)
config = ConfigParser.RawConfigParser()
config.read(iniPath)

for name in names:
	path = basePath + os.sep + name + ".tif"
	print(path)
	fMag     = config.getfloat(name, "Mag")
	fScaleX  = config.getfloat(name, "ScaleX")
	fScaleY  = config.getfloat(name, "ScaleY")
	sUnits   = config.get(name, "Units")
	if (bConvertNmToUm == True):
		if(sUnits == "nm"):
			fScaleX /= 1000.
			fScaleY /= 1000.
			sUnits =  mu + "m"
	if(sUnits == "µm"):
		sUnits =  mu + "m"
	sComment = config.get(name, "Comment")
	strPath = basePath + os.sep + name + ".tif"
	imp = IJ.openImage(strPath)
	cal = imp.getCalibration()
	cal.setXUnit(sUnits)
	cal.setYUnit(sUnits)
	cal.pixelWidth = fScaleX
	cal.pixelHeight = fScaleY
	obinfo = imp.getProperty("Info")
	sMag = "Mag: %.1f X, " % fMag
	newInfo = "Microscope: " + sMicroscope + " Software: AnalySIS.0, User: " + sUser +  "\n" + sMag + sComment
	imp.setProperty("Info", newInfo)
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


print("done")



