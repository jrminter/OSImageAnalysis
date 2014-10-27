# 4-WB-FinalImg_.py
#
# White balance the shading corrected image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-25  JRM 0.1.00  Initial prototype
# 2014-10-27  JRM 0.1.100 Use IJ images

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager

imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1/out"
strImg = imgDir + relImg + "/bez-50X-1-ij-edf-sc.tif"

# 1. Open an image
impExp = IJ.openImage(strImg)
impExp.show()

# 2. Add a rectangle for white balance
IJ.makeRectangle(0, 190, 1600, 260)

# 3. Do the work
jmg.whiteBalance(impExp)

# 4. save the results
out = WindowManager.getCurrentImage()
name = out.getShortTitle()
strImg = imgDir + relImg + "/" + name + ".tif"
IJ.saveAs("Tiff", strImg)



