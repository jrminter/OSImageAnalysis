# procRGB_.py
#
# proess an RGB image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-21  JRM 0.1.00  Initial prototype
# 2014-10-22  JRM 0.1.10  Finally got to work and moved flatFieldCorrectRGB
#                         into jmFijiGen.py. TO DO: add error checking

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ


imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1/ff"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg = imgDir + relImg + "/sis-efi.tif"
print(strImg)
strFF  = imgDir + relImg + "/gain.tif"

# 1. Open an image and it's flat field
impExp = IJ.openImage(strImg)
impExp.show()
impBkg  =  IJ.openImage(strFF)

impSc = jmg.flatFieldCorrectRGB(impExp, impBkg)

impSc.show()









