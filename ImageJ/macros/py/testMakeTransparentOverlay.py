from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os, time
from ij import IJ
import jmFijiGen as jmg



homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
ePrjDir    = "QM14-04-04D1-Steele"
sampID     = "qm-04227-49G003-456-R-15-FIB"
mapID      = "7kV-map4"   
datDir     = "/Oxford/" + ePrjDir + "/reports/" + sampID + "/" + sampID + "-" + mapID
relWrk     = datDir + "/work"
wrkDir     = edsDir + relWrk

strROI = wrkDir + "/" + "ROI.png"
impRoi = IJ.openImage(strROI)

lName   = ["O-K","Cu-L", "P-K", "Pd-L", "Ag-L"]

for name in lName:
  strImg = wrkDir + "/" + name +".png"
  impExp = IJ.openImage(strImg)
  impOvr = jmg.makeFlattenedTransparentOverlay(impRoi, impExp, op=50)
  impOvr.show()
  strImg = wrkDir + "/" + name +"-ROI.png"
  if os.access(strImg, os.R_OK):
    os.remove(strImg)
  IJ.saveAs(impOvr, "PNG", strImg)
  impOvr.close()
  

