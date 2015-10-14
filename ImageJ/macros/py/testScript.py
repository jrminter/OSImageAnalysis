# @DatasetService ds
# @UIService ui
# @File file
# @double(label = "fwMicrons", value = 1.23) fwMicrons
# @double(label = "barWid", value=0.1) barWid
# @int(label = "barHt", value=6) barHt
# @int(label = "barFnt", value=24) barFnt
# @int(label = "barCol", value="Black") barCol
# @String(label = "barLoc", value="Lower Right") barLoc


# autoProcImage2.py
# A quick script to calibrate an Oxford AZtec image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-10-13  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ, Prefs
from ij.io import FileSaver 
import jmFijiGen as jmg
from ij.measure import Calibration


# load the dataset
dataset = ds.open(file.getAbsolutePath())
# display the dataset
ui.show(dataset)
imp = IJ.getImage()
fName = imp.getShortTitle()

print(fName)
imp.changes = False
# imp.close()


