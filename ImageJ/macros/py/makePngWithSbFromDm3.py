# makePngWithSbFromDm3.py
#
# J. R. Minter
#
# Process a folder of .DM3 files and burn scale bars
# expects a subfolder "dm3" in a sample folder
#
# CCA licence
#  date       who  comment
# ----------  ---  -----------------------------------------------------
# 2014-01-09  JRM  initial prototype
# 2015-02-27  JRM  change micron to µm 

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

barW    =     20        # bar width, units
barH    =      6        # bar height, pts
barF    =     28        # bar font, pts
barC    = "Black"       # bar color
barL    = "Lower Right" # bar location

imgRt  = os.environ['IMG_ROOT']
relPrj = "/QM15-02-02C-Brust"
labId  = "qm-04280"
smpId  = "TBB1172-6"



sDm3Path = imgRt + relPrj + "/" + labId + "-" + smpId + "/dm3/"
sPngPath = imgRt + relPrj + "/" + labId + "-" + smpId + "/png/"
jmg.ensureDir(sPngPath)
strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)

query = sDm3Path + "*.dm3"
print(query)
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
  i += 1
  orig = ImagePlus(fi)
  strName = os.path.basename(fi)
  strName = strName.split('.')[0]
  lStr =  strName.split('-')
  l = len(lStr)
  strNum = lStr[l-1]
  iNum = int(strNum)
  orig.setTitle(strNum)
  cal = orig.getCalibration()
  strUnit = cal.getUnit()
  if strUnit == "micron":
    mu = IJ.micronSymbol
    strUnit  = mu + "m"
    cal.setUnit(strUnit)
    orig.setCalibration(cal)
    orig.updateAndRepaintWindow()
  if i == 1:
    # a hack to get the scale bars to work reliably
    foo = orig.duplicate()
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)
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

