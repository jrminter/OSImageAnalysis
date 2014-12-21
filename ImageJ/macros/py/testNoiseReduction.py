# testNoiseReduction.py
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

import jmFijiGen as jmg

def smoothMapImage(imp, no=2):
  """smoothMapImage(imp, no=2)
  Smooths an X-ray map image (typically a 16 bit gray image). First, it sets the
  display range to a noise offset (to get rid of isolated pixels), converts to an 8
  bit image that spans no to 255 and smooths with a 3x3 kernel. and
  converts it to an 8 bit gray scale image that spans 0-255. This is
  ready for a  hueLUT. It peforms this on a duplicate imp and returns
  the resultant imp. To the best of my understanding, this is how Oxford
  treats their maps. 
  Inputs:
  imp - the input ImagePlus object
  no  - the noise offset, default = 2, to remove noise pixels
  Returns:
  ret - an ImapePlus for the 8-bit, scaled, filtered image
  """
  stats = imp.getStatistics(Measurements.MIN_MAX)
  imp.setDisplayRange(no, stats.max)
  ret = imp.duplicate()
  IJ.run(ret, "8-bit", "")
  name = imp.getShortTitle()
  ip = ret.getProcessor()
  ip.smooth()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  ret.setDisplayRange(no, stats.max)
  ret.setTitle(name)
  return ret
  
def clipNoisePixMapImage(imp, no=2):
  """clipNoisePixMapImage(imp, no=2)
  Clips noise pixels from an X-ray map image (typically a 16 bit gray image). 
  First, it sets the isplay range to a noise offset (to get rid of isolated pixels),
  converts to an 8 bit image that spans no to 255 and returns an 8 bit gray scale
  image that spans no-255. This is ready for a  hueLUT. It peforms this on a duplicate
  imp and returns the resultant imp. To the best of my understanding, this is how Oxford
  treats their maps w/o a 3x3 smooth. 
  Inputs:
  imp - the input ImagePlus object
  no  - the noise offset, default = 2, to remove noise pixels
  Returns:
  ret - an ImapePlus for the 8-bit, scaled, filtered image
  """
  stats = imp.getStatistics(Measurements.MIN_MAX)
  imp.setDisplayRange(no, stats.max)
  ret = imp.duplicate()
  IJ.run(ret, "8-bit", "")
  name = imp.getShortTitle()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  ret.setDisplayRange(no, stats.max)
  ret.setTitle(name)
  return ret  


edsDir  = os.environ['EDS_ROOT']
imgPth = edsDir + "/Oxford/QM14-04-03A5-English/reports/qm-04206-Pd8-1-FIB-2/qm-04206-Pd8-1-FIB-2-7kV-map1/tif/Ag-L.tif"
imp = IJ.openImage(imgPth)
ret = jmg.clipNoisePixMapImage(imp, no=3)
ret.show()
