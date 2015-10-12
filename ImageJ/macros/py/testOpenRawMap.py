# openRawMap.py
#
# J. R. Minter
# CCA licence
#
# Open a raw EDS map exported from the AZtec softeware as as an IMAGE cube
# w/o using the GUI. One would need to switch indicies and do the transformation
# described by Zach Gainford in his Bruker example from Microscopy Today Sep 2014 pg75.
# which uses a VECTOR cube.
#
# Note: this was adapted from Albert Cardona's example of how to implement a new file format reader
# http://albert.rierol.net/imagej_programming_tutorials.html#How to integrate a new file format reader and writer
#
#
#  date       who  comment
# ----------  ---  -----------------------------------------------------
# 2015-10-12  JRM  initial prototype. Use env vars for paths. Imported
#                  from jmFijiHen.py
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import jmFijiGen as jmg

# test with the std Oxford paint data set in std location
# homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
rPrjDir = "QM15-01-02A-Minter"
ePrjDir = "QM15-01-02A-Minter"
labId = "qm-04355"
smpId = "Paint-xs"
mapId = "20kV-map1"


datDir = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
rawPat = datDir + "/" + labId + "-" + smpId + "-" +mapId + "/raw/"
rawFil = labId + "-" + smpId + "-" +mapId + ".raw"

print(rawPat)
print(rawFil)

orig = jmg.openRplRawImageCube(rawPat, rawFil, 256, 192, 2048, 0.5156, 10.0, -100.0)
orig.show()








