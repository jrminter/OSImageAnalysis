# openFolderImagesWithLUT.py
#
# Open a folder of stored images apply set display limits
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-01-14  JRM 0.1.00  Initial prototype. Now path separator agnostic


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ, Prefs # , WindowManager
from ij.io import DirectoryChooser, FileSaver

fLo    = 1800.
fHi    = 11000.


lastPath = Prefs.get("Last.Image.Dir", "None")
if os.path.exists(lastPath):
	os.chdir(lastPath)

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()
Prefs.set("Last.Image.Dir", basePath)



jmg.applyGrayLimitsToFolder(basePath, fLo, fHi, ext='.tif')




jmg.openFolderWithSingleLUT(basePath, ext='.tif')

print("done")



