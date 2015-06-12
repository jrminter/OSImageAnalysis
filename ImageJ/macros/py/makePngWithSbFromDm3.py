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

barW    =    0.02        # bar width, microns
barH    =      6        # bar height, pts
barF    =     28        # bar font, pts
barC    = "Black"       # bar color
barL    = "Lower Right" # bar location

imgRt  = os.environ['IMG_ROOT']
relPrj = "/QM15-02-05B-Ferrar"
labId  = "qm-04379"
smpId  = "PGB-2015-065C-bot-an"



sDm3Path = imgRt + relPrj + "/" + labId + "-" + smpId + "/dm3/"
sPngPath = imgRt + relPrj + "/" + labId + "-" + smpId + "/png/"
jmg.ensureDir(sPngPath)


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
    barUseW = barW
  else:
    if strUnit == "nm":
      barUseW = 1000 * barW
    
  strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barUseW, barH, barF, barC, barL)
    
  # a hack to get the scale bars to work reliably
  foo = orig.duplicate()
  IJ.run(foo, "RGB Color", "")
  IJ.run(foo, "Add Scale Bar", strBar)
  foo.close()
  # IJ.run(orig, "Enhance Contrast", "saturated=0.35")
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

