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
from ij.plugin.filter import RankFilters

import jmFijiGen as jmg

def smoothMapImage(imp, no=2):
  """smoothMapImage(imp, no=2)
  Smooths an X-ray map image (typically a 16 bit gray image). First, it sets the
  display range to a noise offset to the max and sets pixels below the noise offset
  to zero (to get rid of isolated pixels), converts to an 8
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
  ip = ret.getProcessor()
  data = ip.getPixels()
  l = len(data)
  for i in range(l):
    val = data[i]
    if val < no:
      data[i] = 0
  IJ.run(ret, "8-bit", "")
  name = imp.getShortTitle()
  ip = ret.getProcessor()
  ip.smooth()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  ret.setDisplayRange(0, stats.max)
  ret.setTitle(name)
  return ret
  
def clipNoisePixMapImage(imp, no=2):
  """clipNoisePixMapImage(imp, no=2)
  Clips noise pixels from an X-ray map image (typically a 16 bit gray image). 
  First, it sets the display range to a noise offset to max and removes the noise
  pixels (to get rid of isolated pixels), then converts to an 8 bit image that spans
  0 to 255 and returns an 8 bit gray scale. This is ready for a  hueLUT. It peforms
  this on a duplicate imp and returns the resultant imp. To the best of my understanding,
  this is how Oxford treats their maps w/o a 3x3 smooth. 
  Inputs:
  imp - the input ImagePlus object
  no  - the noise offset, default = 2, to remove noise pixels
  Returns:
  ret - an ImapePlus for the 8-bit, scaled, filtered image
  """
  stats = imp.getStatistics(Measurements.MIN_MAX)
  imp.setDisplayRange(no, stats.max)
  ret = imp.duplicate()
  ip = ret.getProcessor()
  data = ip.getPixels()
  l = len(data)
  for i in range(l):
    val = data[i]
    if val < no:
      data[i] = 0
  IJ.run(ret, "8-bit", "")
  name = imp.getShortTitle()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  ret.setDisplayRange(0, stats.max)
  ret.setTitle(name)
  return ret  

def rankFilterMapImage(imp, radius=1.5, no=2):
  """clipNoisePixMapImage(imp, no=2)
  Clips noise pixels from an X-ray map image (typically a 16 bit gray image). 
  First, it sets the display range to a noise offset to max and removes the noise
  pixels (to get rid of isolated pixels), then converts to an 8 bit image that spans
  0 to 255 and returns an 8 bit gray scale. This is ready for a  hueLUT. It peforms
  this on a duplicate imp and returns the resultant imp. To the best of my understanding,
  this is how Oxford treats their maps w/o a 3x3 smooth. 
  Inputs:
  imp - the input ImagePlus object
  no  - the noise offset, default = 2, to remove noise pixels
  Returns:
  ret - an ImapePlus for the 8-bit, scaled, filtered image
  """
  stats = imp.getStatistics(Measurements.MIN_MAX)
  imp.setDisplayRange(0, stats.max)
  ret = imp.duplicate()
  ip = ret.getProcessor()
  data = ip.getPixels()
  l = len(data)
  for i in range(l):
    val = data[i]
    if val < no:
      data[i] = 0
  rf = RankFilters()
  rf.rank(ret.getProcessor(), radius, RankFilters.MEDIAN)
  IJ.run(ret, "8-bit", "")
  name = imp.getShortTitle()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  ret.setDisplayRange(0, stats.max)
  ret.setTitle(name)
  return ret 


edsDir  = os.environ['EDS_ROOT']
imgPth = edsDir + "/Oxford/QM14-04-03A5-English/reports/qm-04206-Pd8-1-FIB-2/qm-04206-Pd8-1-FIB-2-7kV-map1/tif/Cu-L.tif"
imp = IJ.openImage(imgPth)
ret = rankFilterMapImage(imp, radius=1.0, no=2)
ret.show()
