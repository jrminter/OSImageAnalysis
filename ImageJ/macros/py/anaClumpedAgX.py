# anaClumpedAgX.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-07-26  JRM 0.1.00  initial prototype development. Note that Fiji 
#                         can read .dm3 files directly. N.B. This version
#                         adds the environment variable 'RPT_ROOT'
# 2014-09-30  JRM 0.1.10  Moved some code to jmFijiGen and edit for ImageJ2
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time
from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg


imgDir  = os.environ['IMG_ROOT']
rptDir  = os.environ['RPT_ROOT']
relImg  = "/test/clumpAgX"
sampID  = "qm-03966-KJL-031"
nmPerPx = 1.213
minCirc = 0.5
minSize = 1.0e1
maxSize = 1.0e6

# set some strings
strScale = "distance=1 known=%.3f pixel=1 unit=nm global" % nmPerPx
strAna   = "size=%g-%g circularity=%.3f-1.00 show=[Overlay Outlines] display exclude clear include" % (minSize, maxSize, minCirc)

sImgPath = imgDir + relImg + "/" + sampID + "/"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)

query = sImgPath + "*.dm3"
lFiles = glob.glob(query)
for fi in lFiles:
  imp = ImagePlus(fi)
  strName = os.path.basename(fi)
  strName = strName.split('.')[0]
  imp.setTitle(strName)
  imp.show()
  IJ.run("Enhance Contrast", "saturated=0.35")
  IJ.run("8-bit")
  IJ.run("Threshold", "method=Default white")
  IJ.run("Watershed")
  IJ.run("Set Measurements...", "area fit shape feret's display redirect=None decimal=5")
  IJ.run("Set Scale...", strScale)
  
  IJ.run("Analyze Particles...", strAna)
  rFiName = strName + ".csv"
  rFiPath = sRptPath + rFiName
  IJ.saveAs("Results", rFiPath)
  imp.changes = False
  imp.close()
