# 01-Prep-qm-nnnnn-sampleID-nnkV-map1.py
#
# Prep images from 01-Prep-qm-nnnnn-sampleID-nnkV-map1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-07  JRM 0.1.00  Use the Hue lut and prep map images for stitching
#                         this version applies gamma to ROI and tries 
#                         to use standard directories.
# 2014-11-07  JRM 0.1.10  Added some test flags to make it easier to debug
#                         directories and image contrast.
# 2014-11-20  JRM 0.1.20  Added option to perform median filter.
# 2014-12-03  JRM 0.1.30  Updated to remove display for headless operation
# 2014-12-09  JRM 0.1.40  replaced imp.flush() with imp.close() to fix bug

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

# start with this True and see that the paths are right, then set to false
bTstPath   = False
# when you are happy with images produces, set to True to save
bSave      = True
# option to do a median filter to reduce noise. Useful if map will not be downscaled later...
bDoMedian  = False
rMedian    = 3.0
# gamma for maps and image. Set to 1 for linear.
gam  = 0.7
gamI = 0.7
# option for no display when True
bHeadless = True

homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
ePrjDir    = "QM14-nn-nnA-Client"
sampID     = "qm-nnnnn-sampleID"
mapID      = "nnkV-map1"   
datDir     = "/Oxford/" + ePrjDir + "/reports/" + sampID + "/" + sampID + "-" + mapID
relIn      = datDir + "/tif"
relOut     = datDir + "/work"
inDir  = edsDir + relIn
outDir = edsDir + relOut

if (bSave != True):
  print(inDir)
  print(outDir)


#           map fills row-by row left to right
lName   = ["C-K", "N-K","O-K","Cu-L", "P-K", "Cl-K", "Pd-L", "Ag-L", "ROI"]
lHue    = [    0,   210,  120,   180,   150,     90,     60,     30 , -1   ]
lGamma  = [  gam,   gam,  gam,   gam,   gam,    gam,    gam,    gam , gamI ]
#        sz   w-px  um
lCal = [193., 1024, -6]



jmg.ensureDir(outDir)

for i in range(len(lName)):
  strImg = inDir + "/" + lName[i] + ".tif"
  if (bTstPath == True):
    print(strImg)
  else:
    imp = IJ.openImage(strImg)
    name = imp.getShortTitle()
    IJ.run(imp, "Enhance Contrast", "saturated=0.35")
    if bDoMedian:
      strMedian = "radius=%g" % rMedian
      IJ.run(imp, "Median...", strMedian)   
    IJ.run(imp, "8-bit", "")
    if bHeadless != True:
      imp.show()
    hue = lHue[i]
    gamma = lGamma[i]
    if (hue >= 0):
      work = jmg.applyHueLUT(imp, hue, gamma, bHeadless=bHeadless)
      imp.changes = False
      imp.close()
      imp = work
      IJ.run(imp, "RGB Color", "")
      imp.setTitle(name)
      imp.changes = False
      if bHeadless != True:
        imp.show()
    else:
      IJ.run(imp, "Gamma...", "value=%g" % gamma)
      IJ.run(imp, "RGB Color", "")
      imp.setTitle(name)
      imp.changes = False
      if bHeadless != True:
        imp.show()
    
    strImg = outDir + "/" + lName[i] + ".png"
    if bSave:
      IJ.saveAs(imp, "PNG", strImg)
      imp.close()
    
    
if bHeadless:
  print("done")
      
  

