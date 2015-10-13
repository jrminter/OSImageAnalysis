# autoProcImage.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-10-13  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ, Prefs
from ij.io import FileSaver 
import jmFijiGen as jmg
from os import path  

sDir = "C:/Data/eds/Oxford/QM15-02-13A1-DiLeo/reports/qm-04493-RAD-2015-0148-untreated-ff/tif/"

def autoProcAZtecImage(fwMicrons, wrkDir, barWid=0.1, barHt=9, barFnt=24, barCol="Black", barLoc="Lower Right"):
	imp = IJ.getImage()
	fName = imp.getShortTitle()
	wid = imp.getWidth()
	argThree = "distance=%g known=%f pixel=1 unit=um" % (wid, fwMicrons)
	IJ.run(imp, "Set Scale...", argThree)
	IJ.run(imp, "Enhance Contrast", "saturated=0.35")
	fs = FileSaver(imp) 
	if path.exists(wrkDir) and path.isdir(wrkDir):
		print "folder exists:", wrkDir
		tifName = fName + ".tif"
		tifPath = path.join(wrkDir, tifName)
		print(tifPath)
		if fs.saveAsTiff(tifPath):
			print "Tif saved successfully at ", tifPath  
				
	IJ.run(imp, "RGB Color", "")
	# dummy to get things set
	foo = imp.duplicate()
	s2 = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barWid, barHt, barFnt, barCol, barLoc)
	IJ.run(foo, "Add Scale Bar", s2)
	# explicitly save preferences
	Prefs.savePreferences()
	foo.changes = False
	foo.close()
	IJ.run(imp, "Add Scale Bar", s2)
	fs = FileSaver(imp) 
	pngName = fName + ".png"
	pngPath = path.join(wrkDir, pngName)
	if fs.saveAsPng(pngPath):
		print "png saved successfully at ", pngPath  


autoProcAZtecImage(5.29, sDir, barWid=0.1,  barCol="White")

