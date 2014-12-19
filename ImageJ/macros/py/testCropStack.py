# testCropStack.py
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os, time
from ij import IJ
from ij.gui import ShapeRoi, Roi
from ij.process import ImageProcessor, StackProcessor

def headlessCropStack(imp, lRoi):
  """headlessCropStack(imp, lRoi)
  Crop a stack to a rectangle given by the list, lRoi
  Inputs:
  imp  - the ImagePlus of the stack to crop
  lRoi - a list with [x0, y0, w, h]
  Returns:
  imp - the ImagePlus of the cropped stack
  """
  ip = imp.getProcessor()
  roi = ShapeRoi(Roi(lRoi[0], lRoi[1], lRoi[2], lRoi[3]))
  imp.setRoi(roi)
  stackSize= imp.getStackSize()
  bounds = roi.getBounds()
  newWidth = bounds.width
  newHeight = bounds.height
  interpolationMethod = ImageProcessor.BICUBIC
  ip.setInterpolationMethod(interpolationMethod)
  sp = StackProcessor(imp.getStack(), ip)
  s2 = sp.resize(newWidth, newHeight, False)
  cal = imp.getCalibration()
  cal.xOrigin -= roi.getBounds().x
  cal.yOrigin -= roi.getBounds().y
  imp.setStack(None, s2)
  imp.setCalibration(cal)
  return imp
  
    
  
  
  
  
  
  
  
  
  
  
  
  ret = imp
  print "done"
  return ret

lRoi = [0, 22, 512, 163]

gitDir   = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/Stack.tif"
imgPath = gitDir + relImg

imp = IJ.openImage(imgPath)
# 512x203
ret =  headlessCropStack(imp, lRoi=lRoi)
ret.show()
# time.sleep(2)
# imp.close()
