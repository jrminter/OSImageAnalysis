# procLatex_.py
#
# Process a Latex image and compute the mean and std dev of the ECD (in px)
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-28  JRM 0.1.00  Translated from .ijm file and updated
# 2014-10-11  JRM 0.1.10  Make sure unexpected scale is removed
# 2014-11-01  JRM 0.2.00  Updated to run in headless mode, if desired

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from java.awt import Rectangle
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
from ij.measure import Measurements
from ij.measure import ResultsTable
from ij.plugin.filter import EDM
from ij.plugin.frame import RoiManager
from ij.plugin.filter import ParticleAnalyzer

from java.lang import Double
import java.io as jio

import jmFijiGen as jmg

def computeMean(ar):
  return sum(ar) / float(len(ar))
  
def computeStdDev(ar, mean):
  s = 0
  for i in range(len(ar)):
    s += pow(ar[i] - mean, 2)
  return sqrt(s / float(len(ar) -1))

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images"
imgPath = gitDir + relImg + "/latex.tif"
rptPath = gitDir + relImg + "/latex-size.csv"

bDoWatershed = False

print("Hello world!")
nmPerPx = 2.02
# delta = 250
delta = 0
ball  = 25
minPx = 25
maxPx = 6000
minCr = 0.80
maxCr = 1.0

raw = IJ.openImage(imgPath)
w = raw.getWidth()
h = raw.getHeight()
cal = raw.getCalibration()
cal.pixelHeight = nmPerPx
cal.pixelWidth  = nmPerPx
cal.setXUnit("nm")
cal.setYUnit("nm")
raw.setCalibration(cal)
strBall = "rolling=%g light sliding" % ball
IJ.run(raw, "Subtract Background...", strBall)
IJ.run(raw, "Median...", "radius=2")
IJ.run(raw, "Auto Threshold", "method=Otsu white")
raw.setRoi(delta,delta,w-(2*delta),h-(2*delta))
IJ.run(raw,"Crop","")
if bDoWatershed:
  IJ.run(raw, "Watershed", "")
# do everything in px
IJ.run(raw, "Set Scale...", "distance=1 known=1 pixel=1 unit=[ px]")
#  sMeas = "area centroid center perimeter shape redirect=None decimal=3"
sMeas = "area perimeter shape redirect=None decimal=3"
IJ.run(raw, "Set Measurements...", sMeas)
s1 = "size=%g-%g pixel " % (minPx, maxPx)
s2 = "circularity=%g-%g " % (minCr, maxCr)
s3 = "show=[Overlay Outlines] display exclude clear include"
s = s1 + s2 + s3
IJ.run(raw, "Analyze Particles...", s)

rt = ResultsTable.getResultsTable()
nMeas = rt.getCounter()
print(nMeas)
aPx  = rt.getColumn(ResultsTable.AREA)
cPx  = rt.getColumn(ResultsTable.CIRCULARITY)
arPx = rt.getColumn(ResultsTable.ASPECT_RATIO)
sPx  = rt.getColumn(ResultsTable.SOLIDITY)

ecdPx = []
for i in range(len(aPx)):
  ecd = 2.0*sqrt(aPx[i]/3.1415926)
  ecdPx.append(ecd)




meanPxECD = nmPerPx * round(computeMean(ecdPx), 2)
sdPxECD = nmPerPx * round(computeStdDev(ecdPx, meanPxECD), 2)
print(meanPxECD, sdPxECD)

# prepare the output file
f=open(rptPath, 'w')
strLine = 'ecd.nm, circ, a.r, solidity\n'
f.write(strLine)
for i in range(len(ecdPx)):
  strLine = "%.2f, %.4f, %.4f, %.4f\n" % (nmPerPx*ecdPx[i], cPx[i], arPx[i], sPx[i] )
  f.write(strLine)
f.close()

