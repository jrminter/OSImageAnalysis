# testRGBtoMontage
# Test a jython function to make a montage of the R,G,B channels, and the RGB image
# This is a replacement for the RGB_to_montage plug-in that does not seem to still exist
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-22  JRM 0.1.00  replacement for the RGB_to_montage plug-in
# 2014-12-03  JRM 0.1.00  this is set up for headless

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
import jmFijiGen as jmg

gitDir = os.environ['GIT_HOME']
sPath  = gitDir + "/OSImageAnalysis/images/lena-std.tif"

# make an input RGB image
rgb = IJ.openImage(sPath)
rgb.show()

a = jmg.RGBtoMontage(rgb, bHeadless=True)
a.show()




