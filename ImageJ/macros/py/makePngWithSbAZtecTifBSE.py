# makePngWithSbAZtecTifBSE.py
#
# J. R. Minter
#
# Process a folder of AZtec.tif of BSE imagefiles and burn scale bars
# expects a subfolder "tif" in a sample folder. Test for annotated images
#
# CCA licence
#	date			 who	comment
# ----------	---	-----------------------------------------------------
# 2015-08-06	JRM	initial prototype. Assumes nLo low mag images and the
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
rPrjDir = "QM15-02-10A-Scheibel"
ePrjDir = "QM15-02-10A1-Scheibel"
labId = "qm-04419"
smpId = "PDR11-033"
nLo = -1			# no Lo mag images
fwLo = 57.9	# µm
fwHi = 28.9	# µm
gFac = 0.65 # gamma factor
sFac = 0.05 # saturation factor

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sTifPath = datDir + "/tif/"
sPngPath = datDir + "/png/"

sGamma = "value=%.2f" % gFac
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
	if (i <= nLo):
		jmg.calibImage(orig, fwLo, units=-6)
	else:
		jmg.calibImage(orig, fwHi, units=-6)
	strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
	# a hack to get the scale bars to work reliably
	foo = orig.duplicate()
	if lStr[l-1][0:2] == "an":
		IJ.run(orig, "Enhance Contrast", sSat)
		IJ.run(orig, "RGB Color", "")
		IJ.run(orig, "Add Scale Bar", strBar)
		orig.show()
	else:
		IJ.run(orig, "Gamma...", sGamma)
		IJ.run(orig, "Enhance Contrast", sSat)
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

