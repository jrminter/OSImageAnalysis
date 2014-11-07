# testApplyHueLUT_.py
#
# Test the generation and application of a LUT based upon hue angle
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-06  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
import jmFijiGen as jmg

bInvert = True
gitDir = os.environ['GIT_HOME']
edsDir = os.environ['EDS_ROOT']
relImg = "/OSImageAnalysis/images"
imgPath = gitDir + relImg + "/blobs.gif"
# relImg = "/Oxford/QM14-04-06A2-Wansha/reports/qm-04215-49G003-S-406-F-Bez2-20kV-map2/tif"
# imgPath = edsDir + relImg + "/Ag-L.tif"
print(imgPath)

raw = IJ.openImage(imgPath)
name = raw.getShortTitle()
if bInvert:
  # we need to invert the blob imgage
  IJ.run(raw, "Invert","")
raw.show()

new = jmg.applyHueLUT(raw, 210.0, gamma=0.5)
new.setTitle(name+"-lut")
new.show()



