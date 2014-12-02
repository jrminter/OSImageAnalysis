# testScale.py

import os
from ij import IJ
from ij.process import ImageProcessor
from ij.measure import Calibration

def scaleImg(imp,factor):
  """scaleImg(imp,factor)
  Scale an input ImagePlus for an image by factor using bicubic interpolation. returns an ImagePlus"""
  name = imp.getShortTitle()
  averageWhenDownsizing = True
  im = ImageProcessor.BICUBIC
  newWidth = int(round(factor*imp.getWidth(), 0))
  newHeight = int(round(factor*imp.getHeight(), 0))
  ip = imp.getProcessor()
  ip.setBackgroundValue(0)
  imp2 = imp.createImagePlus()
  imp2.setProcessor(name, ip.resize(newWidth, newHeight, averageWhenDownsizing))
  cal = imp2.getCalibration()
  cal.pixelWidth *= 1.0/factor
  cal.pixelHeight *= 1.0/factor  
  return imp2
  
  
  
  

gitDir  = os.environ['GIT_HOME']
imgPath = gitDir + "/OSImageAnalysis/images/blobs.gif"
imp = IJ.openImage(imgPath)
imp.show()

imp2 = scaleImg(imp, 0.5)
imp2.show()

print(imp)