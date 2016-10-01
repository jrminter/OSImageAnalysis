# @string(label = "CSV File") csvPath
# @boolean(label = "append") bAppend
# @boolean(label = "debug", value=False) bDebug
# @int(label = "line width", value=2) lw
# @int(label = "offset", value=-30) offset
# @int(label = "digits", value=-3) digits
# @int(label = "font", value=18) font
#
# measureLengthWrapper.py
#
# Measure lengths in a series of image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-08-04  JRM 0.1.00  Initial prototype.
# 2016-08-23  JRM 0.1.10  Fixed?

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ, Prefs, WindowManager
from java.awt import Color, Font
import csv
from ij.io import FileSaver, DirectoryChooser
import ConfigParser

imp = IJ.getImage()
jmg.measureFeatureLength(imp, lw, csvPath, bAppend, offset, digits,
                         font, Color.YELLOW, Color.WHITE, bDebug)

