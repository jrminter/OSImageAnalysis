# @string(label = "CSV File") csvPath
# @boolean(label = "append") bAppend
# @boolean(label = "debug", value=False) bDebug
# @double(label = "line width", value=2) lw
# @double(label = "offset", value=-30) offset
# @double(label = "digits", value=-3) digits
# @double(label = "font", value=18) font

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
measureLengthWrapper.py

Measure lengths in a series of image

Modifications

  Date      Who  Ver                       What
----------  --- ------  ------------------------------------------------
2016-08-04  JRM 0.1.00  Initial prototype.
2016-08-23  JRM 0.1.10  Fixed?
2017-04-12  JRM 0.1.10  PEP8 + codec as early as possible
"""


import os
from ij import IJ
from java.awt import Color
import jmFijiGen as jmg


imp = IJ.getImage()

jmg.measureFeatureLength(imp, int(lw), csvPath, bAppend, int(offset),
                         int(digits), int(font),
                         Color.YELLOW, Color.WHITE, bDebug)

