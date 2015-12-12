# procAnalySIScsv.py
#
# Read a .csv file written by the Imaging C Module 'WriteImageInfoFolder'
# reading the image name, magnification, X- and Y-axis scales and unit strings.
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

basePath = '/Users/jrminter/dat/images/test/qm-04570-1421DJD-04-C03/'
csvPath = basePath + '1421DJD-04-C03-SegA-01.csv'
os.chdir(basePath)

f = open(csvPath, 'rb')
data = csv.reader(f, delimiter=',')
i = 0
for row in data:
	i+=1
	# print(len(row))
	if (i < 2):
		print(row[4])
	if (i > 1):
		strName = row[0]
		strPath = basePath + strName + ".tif"
		fMag = float(row[1])
		fScaleX = float(row[2])
		fScaleY = float(row[3])
		strUnits = row[4]
		if (strUnits == "nm"):
			mu = IJ.micronSymbol
			strUnits = mu + "m"
			fScaleX /= 1000.
			fScaleY /= 1000.	
			
		imp = IJ.openImage(strPath)
		cal = imp.getCalibration()
		cal.setXUnit(strUnits)
		cal.setYUnit(strUnits)
		cal.pixelWidth = fScaleX
		cal.pixelHeight = fScaleY
		imp.show()
		time.sleep(1)

		imp.changes = False
		fs = FileSaver(imp)
		if fs.saveAsTiff(strPath):
			print "Tif saved successfully at ", strPath
		
		
		imp.close()
		
		print(strUnits)
		# print(row[3])



print("done")



