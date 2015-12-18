# writeBareOxfordMetadataIni.py
#
# Write a bare metadata file to use to calibrate Oxford AZtec image files
# This version uses the BF&I approach to write the .ini file to get
# the order right... We can edit this to add specific data for individual images
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-16  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij.io import DirectoryChooser

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()

iniPath = basePath + os.sep + 'ImageMetadata.ini'

fMag     = 65000.
fScaleX  = 0.0043457
fScaleY  = 0.0055148
sUnit    = "µm"
sComment = "7 kV, S4, 5 mm, UHR TLD SE+BSE, tilt 52 deg"

names = []

for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append(name)

names.sort()

# open the ini file
f=open(iniPath, 'w')

for name in names:
	print(name)
	strLine = "[" + name + "]"
	f.write(strLine +'\n')
	strLine = "Mag = %.1f" % fMag
	f.write(strLine +'\n')
	strLine = "ScaleX = %.6f" % fScaleX
	f.write(strLine +'\n')
	strLine = "ScaleY = %.6f" % fScaleY
	f.write(strLine +'\n')
	strLine = "Units = %s" % sUnit
	f.write(strLine +'\n')
	strLine = "Comment = %s" % sComment
	f.write(strLine +'\n')
	# write a space between sections
	f.write('\n')

f.close()

print('done')
