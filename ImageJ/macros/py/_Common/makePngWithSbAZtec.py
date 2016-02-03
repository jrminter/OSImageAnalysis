# makePngWithSbAZtec.py
#
# J. R. Minter
#
# Process a folder of calibrated AZtec.tif files and burn scale bars
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-02-02  JRM  Works with a directory chooser


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg


tic = time.time()

sUser = "J. R. Minter"
sMicroscope = "FEI Sirion D5557"
barH = 6						# bar height, pts
barF = 24						# bar font, pts
barC = "White"			# bar color
barL= "Lower Right"	# bar location

gSatFac = 0.01
gLo = 3086
gHi = 14047
bSetGrayLevels = False
bDoTiltCorrect = False


mu = IJ.micronSymbol
scaUm	= mu + "m"


lastPath = Prefs.get("Last.Image.Dir", "None")
if os.path.exists(lastPath):
	os.chdir(lastPath)

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()
Prefs.set("Last.Image.Dir", basePath)

names = []
for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

for name in names:
	path = basePath + os.sep + name + ".tif"
	print(path)

sPngPath = basePath + "/png/"

print(basePath)

jmg.ensureDir(sPngPath)

mu = IJ.micronSymbol
scaUm	= mu + "m"


query = basePath + "*.tif"
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
	orig.setTitle(strName)
	cal = orig.getCalibration()
	u = cal.getUnit()
	pw = cal.pixelWidth
	if u == scaUm:
		if (pw <= 0.02):
			barW =  0.10  # bar width, microns
		elif (pw < 0.06):
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

