# testMakeStackFromImageFiles.py
#
# Make a stack of images from a list of files
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-12-14  JRM 0.1.00  Make a stack of images from a list of files
#                         Note: this illustrates the problem of display
#                         of stacks with very different intensity slices

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ, ImagePlus, ImageStack

homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
ePrjDir    = "QM14-nn-nnA-Client"
sampID     = "qm-nnnnn-sampleID"
mapID      = "nnkV-map1"   
datDir     = "/Oxford/" + ePrjDir + "/reports/" + sampID + "/" + sampID + "-" + mapID
relIn      = datDir + "/tif"
relOut     = datDir + "/work"
inDir  = edsDir + relIn

def makeStackFromImageFiles(lNames, imgDir, stkName='stack', ext='.tif'):
  """makeStackFromImageFiles(lNames, imgDir, stkName='stack', ext='.tif')
  Construct a stack of images from a list of file names
  Inputs:
  lNames  - a list of base file namers
  imgDir  - a path to the image files
  stkName - the name for the stack (default stack)
  ext     - file extension (default .tif)
  Returns:
  An ImagePlus for the stack"""
  strImg = imgDir + "/" + lNames[0] + ext
  imp = IJ.openImage(strImg)
  newStack = ImageStack(imp.getWidth(), imp.getHeight())
  for name in lNames:
    strImg = imgDir + "/" + name + ext
    imp = IJ.openImage(strImg)
    newStack.addSlice(name, imp.getProcessor())
  ret = ImagePlus(stkName, newStack)
  IJ.run(ret, "Enhance Contrast", "saturated=0.35")
  return ret
    
    

lNames = ["C-K", "N-K","O-K", "Cu-L", "P-K", "Cl-K", "Pd-L", "Ag-L", "ROI"]

theStack = makeStackFromImageFiles(lNames, inDir, stkName='stack', ext='.tif')
theStack.show()



print("done")

