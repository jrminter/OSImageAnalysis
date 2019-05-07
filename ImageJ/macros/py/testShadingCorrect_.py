# testShadingCorrect_.py
#
# Correct an image for uneven illumination, From section 10 in
# http://www.ini.uzh.ch/~acardona/fiji-tutorial/
# changed nomenclature to match Gatan's gain normalization 
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-05-05  JRM 0.1.00  testShadingCorrection legacy plug-in

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
import jmFijiGen as jmg
import ShadingCorrect


# gitDir  = os.environ['GIT_HOME']
# relImg  = "/OSImageAnalysis/images"
# strImg  = gitDir + relImg + "/bridge.gif"
# strImg  = gitDir + relImg + "/latex.tif"
imgDir  = os.environ['IMG_ROOT']

strImg  = imgDir + "/key-test/bkg/nonuniform.tif"
print(strImg)

# 1. Open an image 
imp =  IJ.openImage(strImg)
ShadingCorrect()
imp.show()
