# makePngWithSbAZtecTif.py
#
# J. R. Minter
#
# Process a folder of AZtec.tif files and burn scale bars
# expects a subfolder "tif" in a sample folder
#
# CCA licence
#	date			 who	comment
# ----------	---	-----------------------------------------------------
# 2015-07-31	JRM	initial prototype. Assumes nLo low mag images and the
#									rest are high mag. Assumes my "standard" Oxford
#									project structure.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

barW = 1						# bar width, microns
barH = 6						# bar height, pts
barF = 28						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
imgRt = os.environ['IMG_ROOT']
rPrjDir = "QM15-02-08A-Pyszczek"
ePrjDir = "QM15-02-08A2-Pyszczek"
labId = "qm-04411"
smpId = "EP15-193-D"
nLo = 3			# num Lo mag images
fwLo = 57.9	# µm
fwHi = 28.9	# µm

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sTifPath = datDir + "/tif/"
sPngPath = datDir + "/png/"

print(sTifPath)

jmg.ensureDir(sPngPath)


query = sTifPath + "*.tif"
print(query)
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
	i += 1
	fi = fi.replace("\\", "/")
	print(fi)
	orig = ImagePlus(fi)
	strName = os.path.basename(fi)
	strName = strName.split('.')[0]
	lStr = strName.split('-')
	l = len(lStr)
	strNum = lStr[l-1]
	iNum = int(strNum)
	print(strNum)
	orig.setTitle(strNum)
	# orig.show()
	if (i <= nLo):
		jmg.calibImage(orig, fwLo, units=-6)
	else:
		jmg.calibImage(orig, fwHi, units=-6)
	strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
	# a hack to get the scale bars to work reliably
	foo = orig.duplicate()
	IJ.run(foo, "RGB Color", "")
	IJ.run(foo, "Add Scale Bar", strBar)
	foo.close()
	IJ.run(orig, "Enhance Contrast", "saturated=0.35")
	IJ.run(orig, "RGB Color", "")
	IJ.run(orig, "Add Scale Bar", strBar)
	orig.show()
	outPth = sPngPath + strName + ".png"
	IJ.saveAs(orig, "PNG", outPth)
	time.sleep(1)
	orig.close()

toc = time.time()

elapsed = toc - tic

print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )

