# rotate180.py
#
# Rotate the current image plus by 180 deg
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-10-10  JRM 0.1.00  For when you need to flip an image...

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
 
imp = IJ.getImage()

IJ.run(imp, "Rotate... ", "angle=180 grid=1 interpolation=Bicubic");
imp.updateAndRepaintWindow()
