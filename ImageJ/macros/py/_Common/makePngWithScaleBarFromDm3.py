# makePngWithScaleBarFromDm3.py
#
# J. R. Minter
#
# Process a folder of .DM3 files create 16 bit TIF files for ImageJ
# expects a subfolder "dm3" in a sample folder and puts tifs in
# "tif" subfolder
#
# CCA licence
#  date       who  comment
# ----------  ---  -----------------------------------------------------
# 2016-02-01 JRM  initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

imgRt  = os.environ['IMG_ROOT']
relPrj = "/QM16-01-02B-Lofftus"
labId  = "qm-04769"
smpId  = "JLM2016-048"

sDm3Path = imgRt + relPrj + "/" + labId + "-" + smpId + "/dm3/"
sPngPath = imgRt + relPrj + "/" + labId + "-" + smpId + "/png/"
jmg.ensureDir(sPngPath)
mu = IJ.micronSymbol
strMicron  = mu + "m"
barH = 6                # bar height, pts
barF = 24				# bar font, pts
barC = "White"			# bar color
barL = "Lower Right"	# bar location

query = sDm3Path + "*.dm3"
print(query)
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
	i += 1
	orig = ImagePlus(fi)
	orig.show()
	strName = os.path.basename(fi)
	strName = strName.split('.')[0]
	orig.setTitle(strName)
	cal = orig.getCalibration()
	strUnit = cal.getUnit()
	pw = cal.pixelWidth
	ph = cal.pixelHeight
	if strUnit == "micron":
		cal.setUnit(strMicron)
		orig.setCalibration(cal)
		orig.updateAndRepaintWindow()
	if strUnit == "nm":
		cal.setUnit(strMicron)
		pw /= 1000.
		cal.pixelWidth = pw
		ph /= 1000.
		cal.pixelHeight = ph
		orig.setCalibration(cal)
		orig.updateAndRepaintWindow()
	if pw < 0.005:
		barW = 0.10  # bar width, microns
	else:
		barW =  1.0  # bar width, microns
	strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
	# a hack to get the scale bars to work reliably
	foo = orig.duplicate()	
	IJ.run(foo, "RGB Color", "")
	IJ.run(foo, "Add Scale Bar", strBar)
	foo.close()
	IJ.run(orig, "RGB Color", "")
	IJ.run(orig, "Add Scale Bar", strBar)
	orig.show()
	outPth = sPngPath + strName + ".png"
	IJ.saveAs(orig, "PNG", outPth)
	time.sleep(1)
	orig.close()


  	
  

