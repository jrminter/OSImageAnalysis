# calibImage_.py
#
# Apply a calibration to an image from the full width
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-15  JRM 0.1.00  Get'er done

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager

# full width in microns
fw = 57.9

impCal = WindowManager.getCurrentImage()
impCal = jmg.calibImage(impCal, fw, units=-6)
impCal.show()



