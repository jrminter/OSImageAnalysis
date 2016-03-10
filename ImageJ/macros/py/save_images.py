# saveImages.py
#
# J. R. Minter
#
# Process a folder of AZtec.tif files and burn scale bars
# expects a subfolder "tif" in a sample folder
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-01-27  JRM  From S: Drive


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ, WindowManager
import time

theDir = "/Users/jrminter/Downloads/rutgers/"
for i in range(42):
	st = "latex%04d" % (i+1)
	fi = "latex%02d" % (i+1)
	# print(fi)
	imp = WindowManager.getImage(st)
	if(imp != None):
		outPth = theDir + fi + ".png"
		IJ.saveAs(imp, "PNG", outPth)
		time.sleep(1)
		imp.close()
		
	


