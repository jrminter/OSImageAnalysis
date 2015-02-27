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
# 2014-10-02  JRM 0.2.00  Example using flatField() from jmFijiGen.py

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
import jmFijiGen as jmg


# gitDir  = os.environ['GIT_HOME']
# relImg  = "/OSImageAnalysis/images"
# strImg  = gitDir + relImg + "/bridge.gif"
# strImg  = gitDir + relImg + "/latex.tif"
imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/ff-test/TiO2-Ruler/tif"
strImg  = gitDir + relImg + "/TiO2-Ruler-20X-1.tif"
print(strImg)
  
# 1. Open an image 
imp =  IJ.openImage(strImg)
imp.show()
IJ.run("Enhance Contrast", "saturated=0.35")

# flatField(theImp, scaFac=0.25, bShowIntermediate=False)
impCor = jmg.flatField(imp)
impCor.show()