# makePngWithSbAZtecTif.py
#
# J. R. Minter
#
# Process a folder of AZtec.tif files and burn scale bars
# expects a subfolder "tif" in a sample folder
#
# CCA licence
#  date       who   vomment
# ----------  ---	-----------------------------------------------------
# 2015-08-05  JRM	Set up for Loftus qm-04414
# 2015-08-18  JRM	set up for Loftus qm-04429
# 2015-08-21  JRM	set up for Loftus qm-04432
# 2015-08-25  JRM	set up for Loftus qm-04437
# 2015-08-26  JRM	set up for Huang  qm-04440-42
# 2015-09-29  JRM   ability to set gray levels


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

bDoTiltCorrect = False
tiltDeg = 45.0


bDoMedianFilter = False # True to run a median filter
radMF = 1.0            # filter radius

# true to set manual gray levels
bSetGrayLevels = False # Rollins
gLo = 3086
gHi = 14047
gSatFac = 0.01

# barW = 1						# bar width, microns set from list...
barH = 6						# bar height, pts
barF = 28						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
imgRt = os.environ['IMG_ROOT']
rPrjDir = "QM15-02-08A-Pyszczek"
ePrjDir = "QM15-02-08A4-Pyszczek"
labId = "qm-04509"
smpId = "PDR11-246-1"
nVLo  =   -1  # num vLo mag images
nLo   =    3  # num Lo mag images
fwvLo = 289		# µm
fwLo  = 57.9	# µm
fwHi  = 28.9	# µm Lofftus
# fwHi  = 11.6	# µm Rollins

lBarW = [10.0, 5.0, 1.0]

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
	# iNum = int(strNum)
	print(strNum)
	orig.setTitle(strNum)
	# orig.show()
	if (i <= nVLo):
		jmg.calibImage(orig, fwvLo, units=-6)
		barW = lBarW[0]
	else:
		if (i <= nLo+nVLo):
			jmg.calibImage(orig, fwLo, units=-6)
			barW = lBarW[1]
		else:
			jmg.calibImage(orig, fwHi, units=-6)
			barW = lBarW[2]

	strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
	# a hack to get the scale bars to work reliably
	foo = orig.duplicate()
	if (bSetGrayLevels == True):
		IJ.setMinAndMax(foo, gLo, gHi)	
	IJ.run(foo, "RGB Color", "")
	IJ.run(foo, "Add Scale Bar", strBar)
	foo.close()
	if(bDoMedianFilter == True):
		IJ.run(orig, "Median...", "radius=%g" % radMF)

	if (bSetGrayLevels == True):
		IJ.setMinAndMax(orig, gLo, gHi)
	else:
		sArgSat = "saturated=%.2f" % gSatFac
		IJ.run(orig, "Enhance Contrast", sArgSat)

	if(bDoTiltCorrect == True):
		orig = jmg.correctForeshortening(orig, tiltDeg)
		orig = IJ.getImage()
	
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

