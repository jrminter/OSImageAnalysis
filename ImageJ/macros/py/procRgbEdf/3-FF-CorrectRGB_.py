# 3-FF-CorrectRGB_.py
#
# correct an RGB image for shading using a gain image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-21  JRM 0.1.00  Initial prototype
# 2014-10-22  JRM 0.1.10  Finally got to work and moved flatFieldCorrectRGB
#                         into jmFijiGen.py. TO DO: add error checking
# 2014-10-27  JRM 0.1.20  Renamed to make a consistent set

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ


imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg = imgDir + relImg + "/out/bez-50X-1-ij-edf.tif"
print(strImg)
strFF  = imgDir + relImg + "/ff/gain.tif"

# 1. Open an image and it's flat field
impExp = IJ.openImage(strImg)
name = impExp.getShortTitle()
impExp.show()
impBkg  =  IJ.openImage(strFF)

impSc = jmg.flatFieldCorrectRGB(impExp, impBkg)

impSc.show()
name = name + "-sc"
impSc.setTitle(name)


strImg = imgDir + relImg + "/out/" + name + ".tif"
IJ.saveAs("Tiff", strImg)










