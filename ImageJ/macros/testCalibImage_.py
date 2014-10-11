# testCalibImage_.py
#
# Test calibration of the image using calibImage in jmFijiGen.py
# Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-10  JRM 0.1.00  initial prototype development using bugs

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
import jmFijiGen as jmg

gitDir  = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/EC-bse-10kV.png"
fw      = 4.45 # microns

imgPath = gitDir + relImg
print(imgPath)

raw = IJ.openImage(imgPath)

raw = jmg.calibImage(raw, fw, units=-6)
raw.show()
