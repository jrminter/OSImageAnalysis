# TestFindIzero.py
#
# Find the high peak in the histogram
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-18  JRM 0.1.00  Initial test am image extracted from a PowerPoint
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
import jmFijiGen as jmg

imp = IJ.getImage()
iZ = jmg.findI0(imp)
print(iZ)

