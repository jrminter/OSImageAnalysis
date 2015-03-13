# makeTif16FromDm3.py
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
# 2014-03-03 JRM  initial prototype

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
relPrj = "/Kateeva-15-01"
labId  = "qm-04309"
smpId  = "R31"



sDm3Path = imgRt + relPrj + "/" + labId + "-" + smpId + "/dm3/"
sTifPath = imgRt + relPrj + "/" + labId + "-" + smpId + "/tif/"
jmg.ensureDir(sTifPath)

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
  # IJ.run(orig, "Enhance Contrast", "saturated=0.35")
  IJ.run(orig, "16-bit", "")
  orig.show()
  outPth = sTifPath + strName + ".tif"
  IJ.saveAs(orig, "Tiff", outPth)
  time.sleep(1)
  orig.close()

toc = time.time()

elapsed = toc - tic

print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )

