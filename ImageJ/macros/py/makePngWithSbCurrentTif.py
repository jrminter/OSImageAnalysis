# makePngWithSbCurrentTif.py
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
# 2015-10-19	JRM	initial prototype.
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver
import jmFijiGen as jmg

tic = time.time()

bSetMinMax = True
gMin =   500.
gMax = 11600.

barW = 1						# bar width, microns
barH = 6						# bar height, pts
barF = 28						# bar font, pts
barC = "White"			# bar color
barL= "Lower Left"	# bar location

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
# imgRt = os.environ['IMG_ROOT']
# rPrjDir = "QM15-09-02B-Rollins"
ePrjDir = "QM15-02-06B2-Wei"
labId = "qm-04499"
smpId = "282-14-81-face-off"

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sPngPath = datDir + "/png/"
jmg.ensureDir(sPngPath)

orig = IJ.getImage()
ti = orig.getShortTitle()

strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
# a hack to get the scale bars to work reliably
IJ.run(orig, "RGB Color", "")

# dummy to get things set
foo = orig.duplicate()
IJ.run(foo, "Add Scale Bar", strBar)
# explicitly save preferences
Prefs.savePreferences()
foo.changes = False
foo.close()

# now we can be sure the bar is right
IJ.run(orig, "Add Scale Bar", strBar)
orig.show()
outPth = sPngPath + ti + ".png"

fs = FileSaver(orig)
if fs.saveAsPng(outPth):
	print "png saved successfully at ", outPth  

time.sleep(1)
orig.close()



	
