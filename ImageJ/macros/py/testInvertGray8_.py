# testInvertGray8_.py
#
# Invert an 8-bit grayscale image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-05-06  JRM 0.1.00  testInvertGray8 legacy plug-in

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
import jmFijiGen as jmg
import InvertGray8


# gitDir  = os.environ['GIT_HOME']
# relImg  = "/OSImageAnalysis/images"
# strImg  = gitDir + relImg + "/bridge.gif"
# strImg  = gitDir + relImg + "/latex.tif"
imgDir  = os.environ['IMG_ROOT']



strImg  = imgDir + "/key-test/KMAG/KMag1500Sei.tif"
print(strImg)

# 1. Open an image 
imp =  IJ.openImage(strImg)
imp.show()
# IJ.runPlugIn(imp, "ij.plugin.PNG_Writer", "/Users/jrminter/Desktop/Kmag1500Sei.png"

ip = imp.getProcessor()
IJ.runPlugIn("fiji.InvertGray8", imp);

IJ.runPlugIn("ij.plugin.PNG_Writer", "/Users/jrminter/Desktop/Kmag1500Sei.png")
# IJ.runPlugIn("fiji.InvertGray8", ip);
# print("dir out")
# print(out)
# res = InvertGray8()
# imp.show()
# IJ.runPlugIn(imp, "ij.plugin.PNG_Writer", "/Users/jrminter/Desktop/Kmag1500SeiInv.png")