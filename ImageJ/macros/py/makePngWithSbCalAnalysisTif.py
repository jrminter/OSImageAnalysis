# makePngWithSbCalAnalysisTif.py
#
# J. R. Minter
#
# Process a folder of AZtec tif image files. Calibrate and save the
# TIF files, change to RGB and burn scale bars. Script expects a
# subfolder "tif" in a sample folder. Test for annotated images
#
# CCA licence
#	date			 who	comment
# ----------	---	-----------------------------------------------------
# 2015-12-17	JRM	initial prototype.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time
from ij import IJ
from ij.io import FileSaver, DirectoryChooser
from ij import ImagePlus
from ij.io import FileSaver
import jmFijiGen as jmg

tic = time.time()

sFac = 0.0
barW = 5						# bar width, microns
barH = 6						# bar height, pts
barF = 24						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()

sPngPath = basePath + os.sep + "png" + os.sep
jmg.ensureDir(sPngPath)


names = []

for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

sSat = "saturated=%.2f" % sFac
strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)

for name in names:
	path = basePath + os.sep + name + ".tif"
	print(path)
	orig = ImagePlus(path)
	strName = os.path.basename(path)
	print(strName)
	orig.setTitle(strName)
	orig.show()
	IJ.run(orig, "Enhance Contrast", sSat)
	IJ.run(orig, "RGB Color", "")
	IJ.run(orig, "Add Scale Bar", strBar)
	orig.show()
	pngPath = sPngPath + name + ".png"
	fs = FileSaver(orig)
	if fs.saveAsPng(pngPath):
		print "png saved successfully at ", pngPath
	orig.changes = False
	time.sleep(1)
	orig.close()

print("done")
