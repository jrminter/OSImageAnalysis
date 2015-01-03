# testAnaParticles.py
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

def anaParticles(imp, minSize, maxSize, minCirc, bHeadless=True):
  """anaParticles(imp, minSize, maxSize, minCirc, bHeadless=True)
  Analyze particles using a watershed separation. If headless=True, we cannot
  redirect the intensity measurement to the original immage becuae it is never
  displayed. If we display the original, we can and get the mean gray level. We
  may then compute the particle contrast from the measured Izero value for the image.
  No ability here to draw outlines on the original."""
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
  if bHeadless == True:
    strSetMeas = "area mean modal min center perimeter bounding fit shape feret's decimal=3"
  else:
    imp.show()
    strSetMeas = "area mean modal min center perimeter bounding fit shape feret's redirect='original' decimal=3"
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
bHeadless = False

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

sImgPath = imgDir + relImg + "/" + sampID + "/" + sampID + "-01.dm3"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)
sRptCsvPath = sRptPath + sampID + ".csv"
sRptImgPath = sRptPath + "png/"
jmg.ensureDir(sRptImgPath)


orig = ImagePlus(sImgPath)
strName = os.path.basename(sImgPath)
strName = strName.split('.')[0]
orig.setTitle(strName)
# orig.show()
iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
print(iZero)

[ana, rt] = anaParticles(orig, minSize, maxSize, minCirc, bHeadless=bHeadless)
nMeas = rt.getCounter()
print("%d particles detected in image %d" % (nMeas,1) )
nCols = rt.getLastColumn()
for j in range(nCols+1):
  print(rt.getColumnHeading(j))


print("Area     = %d" % rt.getColumnIndex("Area"))
print("Mean     = %d" % rt.getColumnIndex("Mean"))
print("Perim.   = %d" % rt.getColumnIndex("Perim."))
print("Major    = %d" % rt.getColumnIndex("Major"))
print("Minor    = %d" % rt.getColumnIndex("Minor"))
print("Circ     = %d" % rt.getColumnIndex("Circ."))
print("FeretX   = %d" % rt.getColumnIndex("FeretX"))
print("FeretY   = %d" % rt.getColumnIndex("FeretY"))
print("AR       = %d" % rt.getColumnIndex("AR"))
print("Round    = %d" % rt.getColumnIndex("Round"))
print("Solidity = %d" % rt.getColumnIndex("Solidity"))

rt.show("Results")

print("done")


