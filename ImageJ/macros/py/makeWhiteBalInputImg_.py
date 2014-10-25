# makeWhiteBalInputImg_.py
#
# Make an input image ready for the whiteBalance test
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-25  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1/out"
strImg = imgDir + relImg + "/sis-efi-sc.tif"

# 1. Open an image and it's flat field
impExp = IJ.openImage(strImg)
impExp.show()
IJ.makeRectangle(0, 190, 1600, 260)


