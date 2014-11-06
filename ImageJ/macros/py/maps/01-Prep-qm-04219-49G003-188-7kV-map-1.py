# 01-Prep-qm-04219-49G003-188-7kV-map-1
#
# Prep images from qm-04219-49G003-188-7kV-map-1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-06  JRM 0.1.00  Use the Hue lut and prep map images for stitching

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

bSave      = True
homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
relIn      = "/Oxford/QM14-04-06B-Wansha/reports/qm-04219-493004-188/qm-04219-493004-188-7kV-map1/tif"
relOut     = "/Oxford/QM14-04-06B-Wansha/reports/qm-04219-493004-188/qm-04219-493004-188-7kV-map1/work"
outNamFull = "qm-04209-49G003-S400-F-C21-Bez-10kV-map-2.png"

lName   = ["N-K","O-K","Cu-L", "P-K", "Na-K","Cl-K", "Pd-L", "Ag-L", "ROI"]
lHue    = [    0,  120,   180,   150,   210,    90,     60,     30 , -1   ]
lGamma  = [  1.0,  1.0,   1.0,   1.0,   1.0,   1.0,    1.0,    1.0 , 1.0  ]
#        sz   w-px  um
lCal = [116., 1023, -6]


inDir  = edsDir + relIn
outDir = edsDir + relOut
# jmg.ensureDir(outDir)

for i in range(len(lName)):
  strImg = inDir + "/" + lName[i] + ".tif"
  # print(strImg)
  imp = IJ.openImage(strImg)
  name = imp.getShortTitle()
  IJ.run(imp, "Enhance Contrast", "saturated=0.35")
  IJ.run(imp, "8-bit", "")
  imp.show()
  hue = lHue[i]
  gamma = lGamma[i]
  if (hue >= 0):
    work = jmg.applyHueLUT(imp, hue, gamma)
    imp.changes = False
    imp.close()
    imp = work
    IJ.run(imp, "RGB Color", "")
    imp.setTitle(name)
    imp.changes = False
    imp.show()
  else:
    IJ.run(imp, "RGB Color", "")
    imp.setTitle(name)
    imp.changes = False
    imp.show()
    
  strImg = outDir + "/" + lName[i] + ".png"
  if bSave:
    IJ.saveAs(imp, "PNG", strImg)
    imp.close()
      
  

