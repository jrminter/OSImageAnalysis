# make32bitZeroToOne.py
# 
# Convert an image to a file ready for skimage - 32 bit from 0-1.0
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  ----------------------------------------------
# 2016-01-05  JRM 0.0.90  Initial prototype.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ, ImagePlus


orig = IJ.getImage()
cal = orig.getCalibration()
inf = orig.getProperty("Info")
new = orig.duplicate()
ti = orig.getShortTitle()
IJ.run(new, "32-bit", "")
new.setTitle(ti + "-32")
ip = new.getProcessor()

minV = ip.getMin()
maxV = ip.getMax()
delta = maxV-minV
factor = 1.0/delta

pixels = ip.getPixels()
for i in xrange(len(pixels)):  
  pixels[i] -= minV
  pixels[i] *= factor

new = ImagePlus(ti + "-32", ip)  
new.setDisplayRange(0.0, 1.0)
new.setCalibration(cal)
new.setProperty("Info", inf)

# print(minV, maxV)

new.show()