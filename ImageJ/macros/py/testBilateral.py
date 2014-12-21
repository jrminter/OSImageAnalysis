# testBilateral.py
#
# see https://github.com/fiji/VIB/blob/master/src/main/java/Bilateral_Filter.java
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-12-19  JRM 0.1.00  initial prototype development.
#                         
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ
from ij.process import ImageStatistics
from ij.measure import Measurements
from vib import BilateralFilter

spatialRadius = 20
factor = 5


edsDir  = os.environ['EDS_ROOT']
imgPth = edsDir + "/Oxford/QM14-04-03A5-English/reports/qm-04206-Pd8-1-FIB-2/qm-04206-Pd8-1-FIB-2-7kV-map1/tif/O-K.tif"
imp = IJ.openImage(imgPth)
stats = imp.getStatistics(Measurements.MIN_MAX)
imp.setDisplayRange(stats.min, stats.max)
rangeRadius = factor*(stats.max - stats.min)
stats = imp.getStatistics(Measurements.MIN_MAX)
imp.setDisplayRange(stats.min, stats.max)
IJ.run(imp, "8-bit", "")
imp = BilateralFilter.filter(imp, spatialRadius, rangeRadius)
IJ.run(imp, "Enhance Contrast", "saturated=0.35")
imp.show()
