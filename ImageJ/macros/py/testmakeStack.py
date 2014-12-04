# testMakeStack.py

import os
from ij import IJ, WindowManager, ImageStack, ImagePlus
from ij.io import FileInfo
import jmFijiGen as jmg
  

gitDir = os.environ['GIT_HOME']
sPath  = gitDir + "/OSImageAnalysis/images/lena-std.tif"
# make an input RGB image
lena = IJ.openImage(sPath)
# lena.show()

lI = [lena, lena, lena]

myStack = jmg.makeStackFromListRGB(lI)

myStack.show()



