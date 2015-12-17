# writeBareMetadataIni.py
#
# write a bare metadata file to use to calibrate Oxford image files
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-16  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import ConfigParser

basePath = 'C:/Data/eds/Oxford/QM15-02-19A3-Nelson/reports/qm-04579-SN-655i/tif/'

iniPath = basePath + os.sep + 'ImageMetadata.ini'

config = ConfigParser.RawConfigParser()

names = []

for file in os.listdir(basePath):
	if file.endswith(".tif"):
		name = os.path.splitext(file)[0]
		names.append()

names.sort()

for name in names:
	print(name)
	config.add_section(name)
	config.set(name, "Mag", "35000.0")
	config.set(name, "ScaleX", "0.008076172")
	config.set(name, "ScaleY", "0.008076172")
	config.set(name, "Units", "µm")
	config.set(name, "Comment", "5 kV, S3, 5 mm, UHR ET, tilt -2 deg, C-coated")

# Writing our configuration file to 
configfile = open(iniPath, 'w')
config.write(configfile)
configfile.close()

print('done')
