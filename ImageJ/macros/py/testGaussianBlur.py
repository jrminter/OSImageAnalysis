# testImglib2.py
#
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
from ij.plugin.filter import GaussianBlur

accuracy = 0.001
radius = 3.0
no = 6

edsDir  = os.environ['EDS_ROOT']
imgPth = edsDir + "/Oxford/QM14-04-03A5-English/reports/qm-04206-Pd8-1-FIB-2/qm-04206-Pd8-1-FIB-2-7kV-map1/tif/Cu-L.tif"

imp = IJ.openImage(imgPth)
stats = imp.getStatistics(Measurements.MIN_MAX)
imp.setDisplayRange(no, stats.max)
name = imp.getShortTitle()
ret = imp.duplicate()
ip = ret.getProcessor()
data = ip.getPixels()
l = len(data)
for i in range(l):
  val = data[i]
  if val < no:
    data[i] = 0
IJ.run(ret, "8-bit", "")
ip = ret.getProcessor()
GaussianBlur().blurGaussian(ip, radius, radius, accuracy)
stats = ret.getStatistics(Measurements.MIN_MAX)
ret.setDisplayRange(0, stats.max)
ret.setTitle(name)
ret.show()