# testInvertGray8_.py
#
# Brute force invert an 8-bit grayscale image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-05-06  JRM 0.1.00  testInvertGray8 legacy plug-in

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

import ij
from ij import IJ
import jmFijiGen as jmg
import SingleParticleDetector


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
IJ.run("Invert")

print("dir(ij")
print(dir(ij))

print("dir(SingleParticleDetector")
print(dir(SingleParticleDetector))




