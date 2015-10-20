# calOxfordImg.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-29  JRM 0.1.00  Initial prototype
# 2015-10-19  JRM 0.1.10  let's reproducibly set contrast and save the image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ
from ij.io import FileSaver
import jmFijiGen as jmg

gMin =  4000
gMax = 1200
fwUnits = 4.45
sPath = "C:/Data/eds/Oxford/QM15-06-01D1-Huang/reports/qm-04502-Liberty-NXP-H2O/tif/"

units = IJ.micronSymbol + "m"

imp = IJ.getImage()
imp = jmg.calibImage(imp, fwUnits, units=-6)
IJ.setMinAndMax(gMin, gMax)
imp.updateAndRepaintWindow()

ti = imp.getShortTitle()
fi = sPath + ti + ".tif"
fs = FileSaver(imp)
imp.changes = False
print(fi)
if fs.saveAsTiff(fi):
	print "Tif saved successfully at ", fi  


print("done")
