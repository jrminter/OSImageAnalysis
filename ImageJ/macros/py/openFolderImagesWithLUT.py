# openFolderImagesWithLUT.py
#
# Open a folder of stored images and restore LUT[0]
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
from ij.io import DirectoryChooser


lastPath = Prefs.get("Last.Image.Dir", "None")
if os.path.exists(lastPath):
	os.chdir(lastPath)

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()
Prefs.set("Last.Image.Dir", basePath)

names = []
for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

for name in names:
	path = basePath + os.sep + name + ".tif"
	print(path)
	strPath = basePath + os.sep + name + ".tif"
	imp = IJ.openImage(strPath)
	jmg.useSingleLUT(imp)
	imp.show()


print("done")



