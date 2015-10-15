# makePngWithSbAZtecTifOneMag.py
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
# 2015-10-15	JRM	initial prototype.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
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
barL= "Lower Right"	# bar location

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
# imgRt = os.environ['IMG_ROOT']
# rPrjDir = "QM15-09-02B-Rollins"
ePrjDir = "QM15-02-06B2-Wei"
labId = "qm-04498"
smpId = "SFN-2-face-off"
fwImg = 8.27	# µm
sFac = 0.001 # saturation factor

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sTifPath = datDir + "/tif/"
sPngPath = datDir + "/png/"

sSat = "saturated=%.2f" % sFac

jmg.ensureDir(sPngPath)


query = sTifPath + "*.tif"
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
	i += 1
	fi = fi.replace("\\", "/")
	orig = ImagePlus(fi)
	strName = os.path.basename(fi)
	print(strName)
	orig.setTitle(strName)
	strWrk = strName.split('.')[0]
	lStr = strWrk.split('-')
	l = len(lStr)
	jmg.calibImage(orig, fwImg, units=-6)
	# save the calibrated image
	fs = FileSaver(orig)
	print(fi)
	if fs.saveAsTiff(fi):
		print "Tif saved successfully at ", fi  

	strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
	# a hack to get the scale bars to work reliably
	if (bSetMinMax==True):
		orig.show()
		IJ.setMinAndMax(gMin, gMax)
	else:
		IJ.run(orig, "Enhance Contrast", sSat)
	IJ.run(orig, "RGB Color", "")
	IJ.run(orig, "Add Scale Bar", strBar)
	orig.show()

	outPth = sPngPath + strWrk + ".png"
	fs = FileSaver(orig)
	if fs.saveAsPng(outPth):
		print "png saved successfully at ", outPth  

	time.sleep(1)
	orig.close()

toc = time.time()

elapsed = toc - tic

print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )

