# correctAspectRatioCalibratedActiveImage.py
#
# Correct the aspect ratio in the calibrated active image manually
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  ----------------------------------------------
# 2016-01-05  JRM 0.0.90  Initial prototype.

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
import jmFijiGen as jmg


theImp = IJ.getImage()
arImp = jmg.correctCalibAspectRatio(theImp, False)
arImp.show()