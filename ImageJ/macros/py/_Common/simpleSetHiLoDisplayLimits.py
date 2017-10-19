# simpleSetHiLoDisplayLimits.py
#
# Manually set the Hi and Low display limits for a 16 or 32 bit image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2017-10-1p  JRM 0.0.01  prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time

from ij import IJ, Prefs

gLo = 0
gHi = 24000

orig = IJ.getImage()
bd = orig.getBitDepth()
if(bd==16):
    IJ.setMinAndMax(orig, gLo, gHi)
elif(bd==32):
    IJ.setMinAndMax(orig, gLo, gHi)

