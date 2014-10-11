# exemplarOne_.py
#
# Test creating Float and Byte images using ImageJ1 classes
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-27  JRM 0.1.00  initial prototype development
#                         from http://wiki.imagej.net/Jython_Scripting
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
from ij.gui import HistogramWindow
from ij.measure import Measurements
from ij.measure import ResultsTable
from ij.process import LUT 
from ij.process import ByteProcessor
from ij.process import FloatProcessor
from ij.process import ImageProcessor
from ij.plugin.filter import EDM
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager


from java.util import Random
# don't need to import...
# from java.util import zip
from java.lang import Double
from jarray import zeros

# Explicit float image
imp = ImagePlus("ramp image", FloatProcessor(512, 512))
pix = imp.getProcessor().getPixels()
n_pixels = len(pix)
# catch width
w = imp.getWidth()
  
# create a ramp gradient from left to right
for i in range(len(pix)):
   pix[i] = i % w
  
# adjust min and max, since we know them
imp.getProcessor().setMinAndMax(0, w-1)
imp.show()


# Explicit Byte image

width = 512
height = 512
  
pix = zeros(width * height, 'b')
Random().nextBytes(pix)

channel = zeros(256, 'b')
for i in range(256):
    channel[i] = (i -128) 
cm = LUT(channel, channel, channel)
imp = ImagePlus("Random", ByteProcessor(width, height, pix, cm))
imp.show()

# easy Random
imp = IJ.createImage("Easy Random Image", "8-bit", 512, 512, 1)
Random().nextBytes(imp.getProcessor().getPixels())
imp.show()

# Example watershed
# 1 - Obtain an image
blobs = IJ.openImage("http://imagej.net/images/blobs.gif")
# IJ.run(blobs, "Histogram", "")

# Make a copy with the same properties as blobs image:
imp = blobs.createImagePlus()
hwin = HistogramWindow(blobs)
plotimage = hwin.getImagePlus()


ip = blobs.getProcessor().duplicate()
imp.setProcessor("blobs copy", ip)
 
# 2 - Apply a threshold: only zeros and ones
# Set the desired threshold range: keep from 0 to 74
ip.setThreshold(147, 147, ImageProcessor.NO_LUT_UPDATE)
# Call the Thresholder to convert the image to a mask
IJ.run(imp, "Convert to Mask", "")
 
# 3 - Apply watershed
# Create and run new EDM object, which is an Euclidean Distance Map (EDM)
# and run the watershed on the ImageProcessor:
EDM().toWatershed(ip)
 
# 4 - Show the watersheded image:
imp.show()

# Create a table to store the results
table = ResultsTable()
# Create a hidden ROI manager, to store a ROI for each blob or cell
roim = RoiManager(True)
# Create a ParticleAnalyzer, with arguments:
# 1. options (could be SHOW_ROI_MASKS, SHOW_OUTLINES, SHOW_MASKS, SHOW_NONE, ADD_TO_MANAGER, and others; combined with bitwise-or)
# 2. measurement options (see [http://imagej.net/developer/api/ij/measure/Measurements.html Measurements])
# 3. a ResultsTable to store the measurements
# 4. The minimum size of a particle to consider for measurement
# 5. The maximum size (idem)
# 6. The minimum circularity of a particle
# 7. The maximum circularity
pa = ParticleAnalyzer(ParticleAnalyzer.ADD_TO_MANAGER, Measurements.AREA, table, 0, Double.POSITIVE_INFINITY, 0.0, 1.0)
pa.setHideOutputImage(True)
 
if pa.analyze(imp):
  print "All ok"
else:
  print "There was a problem in analyzing", blobs
 
# The measured areas are listed in the first column of the results table, as a float array:
areas = table.getColumn(0)

# Create a new list to store the mean intensity values of each blob:
means = []
 
for roi in RoiManager.getInstance().getRoisAsArray():
  blobs.setRoi(roi)
  stats = blobs.getStatistics(Measurements.MEAN)
  means.append(stats.mean)

for area, mean in zip(areas, means):
  print area, mean
