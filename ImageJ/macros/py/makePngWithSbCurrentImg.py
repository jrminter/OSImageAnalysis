# makePngWithSbCurrentImg.py
#
# J. R. Minter
#
# Process the current AZtec tif image. Assumes the image has previously
# been calibrated. The script changes the image to RGB , burns a scale
# bar. Script expects a subfolder "png" in a sample folder. It then
# saves a ".png" file. The script assumes the standard EDS folder
# structure for the project. 
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

barW = 1						# bar width, microns
barH = 6						# bar height, pts
barF = 28						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
# imgRt = os.environ['IMG_ROOT']
# rPrjDir = "QM15-09-02B-Rollins"
ePrjDir = "QM15-06-01D1-Huang"
labId = "qm-04501"
smpId = "Liberty-NXP-intact"

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



	
