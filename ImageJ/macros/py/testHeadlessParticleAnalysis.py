# testHeadlessParticleAnalysis.py
#
# Test detection of large and small matte beads from an exemplar image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-18  JRM 0.1.00  Initial test am image of AgX grains
# 2015-01-01  JRM 0.2.00  Using some ideas
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij.measure import ResultsTable, Measurements
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager
import jmFijiGen as jmg

def anaParticles(imp, minSize, maxSize, minCirc):
  strName = imp.getShortTitle()
  imp.setTitle("original")
  ret = imp.duplicate()
  IJ.run(ret, "Enhance Contrast", "saturated=0.35")
  IJ.run(ret, "8-bit", "")
  IJ.run(ret, "Threshold", "method=Default white")
  IJ.run(ret, "Watershed", "")
  rt = ResultsTable()
  # strSetMeas = "area mean modal min center perimeter bounding fit shape feret's redirect='original' decimal=3"
  # N.B. redirect will not work without a displayed image, so we cannot use a gray level image
  strSetMeas = "area mean modal min center perimeter bounding fit shape feret's decimal=3"
  IJ.run("Set Measurements...", strSetMeas)
  # note this doies not get passed directly to ParticleAnalyzer, so
  # I did this, saved everything and looked for the measurement value in ~/Library/Preferences/IJ_Prefs.txt
  # measurements=27355
  # meas = Measurements.AREA + Measurements.CIRCULARITY + Measurements.PERIMETER + Measurements.SHAPE_DESCRIPTORS
  # didn't work reliably
  meas = 27355
  pa = ParticleAnalyzer(0, meas, rt, minSize, maxSize, minCirc, 1.0);
  pa.analyze(ret);
  rt.createTableFromImage(ret.getProcessor())
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
i = 0
for fi in lFiles:
  orig = ImagePlus(fi)
  strName = os.path.basename(fi)
  strName = strName.split('.')[0]
  orig.setTitle(strName)
  # orig.show()
  iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
  print(iZero)
  [ana, rt] = anaParticles(orig, minSize, maxSize, minCirc)
  nMeas = rt.getCounter()
  print("%d particles detected in image %d" % (nMeas,i+1) )
  nCols = rt.getLastColumn()
  lArea   = rt.getColumn(0)
  lPeri   = rt.getColumn(10)
  lMaj    = rt.getColumn(15)
  lMin    = rt.getColumn(16)
  lCirc   = rt.getColumn(18)
  lFeretX = rt.getColumn(29)
  lFerety = rt.getColumn(30)
  lAspRat = rt.getColumn(33)
  lRound  = rt.getColumn(34)
  lSolid  = rt.getColumn(35)
  for j in range(len(lArea)):
    imgOut.append(i+1)
    ecd = 2.0*sqrt(lArea[j]/3.1415926)
    ecdOut.append(ecd)
    cirOut.append(lCirc[j])
    rndOut.append(lRound[j])
    solOut.append(lCirc[j])
    arOut.append(lSolid[j])
  # ana.show()
  i += 1 

# prepare the output file
f=open(sRptCsvPath, 'w')
strLine = 'img, ecd.nm, circ, a.r, round, solidity\n'
f.write(strLine)
for i in range(len(ecdOut)):
  strLine = "%d, %.2f, %.4f, %.4f, %.4f, %.4f\n" % (imgOut[i], ecdOut[i], cirOut[i], arOut[i], rndOut[i], solOut[i] )
  f.write(strLine)

f.close()
print("done")