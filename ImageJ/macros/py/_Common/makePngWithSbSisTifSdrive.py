# makePngWithSbSisTifSdrive.py
#
# J. R. Minter
#
# Process a folder of AZtec.tif files and burn scale bars
# expects a subfolder "tif" in a sample folder
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-01-27  JRM  From S: Drive


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
bSetGrayLevels = False 
gLo = 3086
gHi = 14047
gSatFac = 0.01

barH = 6						# bar height, pts
barF = 24						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

sBaseDir = "S:/Minter/2016/"
rPrjDir = "QM16-06-01A-Dannhauser"
labId = "qm-04617"
smpId = "SUG-primer"



datDir   = sBaseDir + rPrjDir + "/" + labId + "-" + smpId +"/calib/"
sTifPath = datDir
sPngPath = datDir + "/png/"

print(sTifPath)

jmg.ensureDir(sPngPath)

mu = IJ.micronSymbol
scaUm	= mu + "m"


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
	cal = orig.getCalibration()
	u = cal.getUnit()
	pw = cal.pixelWidth
	if u == scaUm:
		if pw <= 0.06:
			barW =  1.0  # bar width, microns
		else:
			barW =  10.0

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

