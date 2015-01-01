# testHeadlessParticleAnalysis.py
#
# Test detection of large and small matte beads from an exemplar image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-18  JRM 0.1.00  Initial test am image of AgX grains
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
import jmFijiGen as jmg

def anaParticles(imp, minSize, maxSize, minCirc):
  strName = imp.getShortTitle()
  ret = imp.duplicate()
  IJ.run(ret, "Enhance Contrast", "saturated=0.35")
  IJ.run(ret, "8-bit", "")
  IJ.run(ret, "Threshold", "method=Default white")
  IJ.run(ret, "Watershed", "")
  strSetMeas = "area modal min perimeter fit shape feret's decimal=3"
  print(strSetMeas)
  IJ.run(ret, "Set Measurements...", strSetMeas)
  strAna   = "size=%g-%g circularity=%.3f-1.00 exclude clear include add" % (minSize, maxSize, minCirc)
  IJ.run(ret, "Analyze Particles...", strAna)
  rt = ResultsTable.getResultsTable()
  nMeas = rt.getCounter()
  print(nMeas)
  ret.setTitle("work")
  ret.changes =  False
  return [ret, rt]
  

col = "red"
wid = 2
bClose = True

imgDir  = os.environ['IMG_ROOT']
rptDir  = os.environ['RPT_ROOT']
relImg  = "/test/clumpAgX"
sampID  = "qm-03966-KJL-031"
nmPerPx = 1.213
minCirc = 0.5
minSize = 1000.0
maxSize = 10000.0

# set some strings
strScale = "distance=1 known=%.3f pixel=1 unit=nm global" % nmPerPx
strAna   = "size=%g-%g circularity=%.3f-1.00 exclude clear include add" % (minSize, maxSize, minCirc)

sImgPath = imgDir + relImg + "/" + sampID + "/"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)
sRptCsvPath = sRptPath + sampID + ".csv"
sRptImgPath = sRptPath + "png/"
jmg.ensureDir(sRptImgPath)

query = sImgPath + "*.dm3"
lFiles = glob.glob(query)
# create empty output vectors for results
imgOut = []
ecdOut = []
cirOut = []
rndOut = []
solOut = []
arOut  = []
gmOut  = []
i = 0
for fi in lFiles:
  if i==0:
    orig = ImagePlus(fi)
    strName = os.path.basename(fi)
    strName = strName.split('.')[0]
    orig.setTitle(strName)
    # orig.show()
    iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
    print(iZero)
    [ana, rt] = anaParticles(orig, minSize, maxSize, minCirc)
    # ana.show()
    
  
  i += 1 

