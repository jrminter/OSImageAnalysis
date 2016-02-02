# @File file
# @boolean(label = "append") bAppend
# @boolean(label = "FIB") bFIB
# @double(label = "imgWid", value=1024) imgWid
# @String(label = "baseName", value="qm-01234-sample") baseName
# @int(label = "kV", value=5) iKV
# @int(label = "spot", value=3) iSpot
# @double(label = "working distance", value = 5.0) dFWD
# @double(label = "tilt Angle", value = 0) dTiltDeg
# @double(label = "magKX", value = 1) magKX
# @double(label = "fwMicrons", value = 1.23) fwMicrons
# @String(label = "detector", value="UHR TLD") sDetector
# @String(label = "Other Comment", value="Lower Right") sOtherComment

# makeAZtecIni.py
# A script to write metadata for an AZtec image to an ini file
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-02-02  JRM 0.1.00  Initial prototype - a work in progress
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ, Prefs
from ij.io import FileSaver 
import jmFijiGen as jmg
from ij.measure import Calibration

print(sOtherComment)
