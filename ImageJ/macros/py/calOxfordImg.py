# calOxfordImg.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-29  JRM 0.1.00  Initial prototype
# 2015-10-19  JRM 0.1.10  let's reproducibly set contrast and save the image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ
from ij.io import FileSaver
import jmFijiGen as jmg

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
ePrjDir = "QM15-06-01C3-Huang"
labId = "qm-04515"
smpId = "Mylan-SP2-MeOH+DPM-72h"

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sTifPath = datDir + "/tif/"

bSetMinMax = True
gMin =  500
gMax = 13700
fwUnits = 5.79


units = IJ.micronSymbol + "m"

imp = IJ.getImage()
imp = jmg.calibImage(imp, fwUnits, units=-6)
if(bSetMinMax == True):
	IJ.setMinAndMax(gMin, gMax)
imp.updateAndRepaintWindow()

ti = imp.getShortTitle()
fi = sTifPath + ti + ".tif"
fs = FileSaver(imp)
imp.changes = False
print(fi)
if fs.saveAsTiff(fi):
	print "Tif saved successfully at ", fi  


print("done")
