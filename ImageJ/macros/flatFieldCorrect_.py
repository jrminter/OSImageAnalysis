# flatFieldCorrect_.py
#
# Correct an image for uneven illumination, From section 10 in
# http://www.ini.uzh.ch/~acardona/fiji-tutorial/
# changed nomenclature to match Gatan's gain normalization 
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-01  JRM 0.1.00  Initial example corrected

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ

from script.imglib.math import Compute, Divide, Multiply, Subtract  
from script.imglib.algorithm import Gauss, Scale2D, Resample  
from script.imglib import ImgLib 

gitDir  = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg  = gitDir + relImg + "/latex.tif"
  
# 1. Open an image 
imp =  IJ.openImage(strImg)
imp.show()
imp.setTitle("raw")
img = ImgLib.wrap(imp)
  
# 2. Simulate a gain image from a Gauss with a large radius  
# (First scale down by 4x, then gauss of radius=20, then scale up)  
# Faster than a big median filter
gain = Resample(Gauss(Scale2D(img, 0.25), 20), img.getDimensions())  
  
# 3. Simulate a perfect dark current  
darkcurrent = 0  
  
# 4. Compute the mean pixel intensity value of the image  
mean = reduce(lambda s, t: s + t.get(), img, 0) / img.size()  

impGain = ImgLib.wrap(gain)
impGain.setTitle("gain")
impGain.show()
IJ.run("Enhance Contrast", "saturated=0.35") 
  
# 5. Correct the illumination  
corrected = Compute.inFloats(Multiply(Divide(Subtract(img, gain),  
                                             Subtract(gain, darkcurrent)), mean))  
  
# 6. ... and show it in ImageJ  
impCor = ImgLib.wrap(corrected)
impCor.setTitle("corrected")
impCor.show()
IJ.run("Enhance Contrast", "saturated=0.35") 

