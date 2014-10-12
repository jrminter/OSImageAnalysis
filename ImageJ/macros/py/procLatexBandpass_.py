# procLatexBndpass_.py
#
# Process a Latex image and compute the mean and std dev of the ECD (in px)
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-28  JRM 0.1.00  Using a bandpass filter to level
#

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
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

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images"
bDoWatershed = False
imgPath = gitDir + relImg + "/latex.tif"
print(imgPath)
rptPath = gitDir + relImg + "/latex-size-bandpass.csv"
print(rptPath)
minPx = 25
maxPx = 6000
minCr = 0.80
maxCr = 1.0
nmPerPx = 2.02


raw = IJ.openImage(imgPath)
raw.show()
# clear any unexpected scale
IJ.run("Set Scale...", "distance=0 known=0 pixel=1 unit=pixel")
IJ.run("Bandpass Filter...", "filter_large=40 filter_small=1 suppress=None tolerance=5 autoscale saturate")
IJ.run("Median...", "radius=3")
IJ.run("Enhance Contrast", "saturated=0.35")
IJ.run("8-bit")
IJ.resetThreshold()
IJ.run("Auto Threshold", "method=Otsu white")
IJ.run("Make Binary")
IJ.run("Convert to Mask")
IJ.run("Invert")
sMeas = "area perimeter shape redirect=None decimal=3"
IJ.run("Set Measurements...", sMeas)
s1 = "size=%g-%g pixel " % (minPx, maxPx)
s2 = "circularity=%g-%g " % (minCr, maxCr)
s3 = "show=[Overlay Outlines] display exclude clear include"
s = s1 + s2 + s3
IJ.run("Analyze Particles...", s)
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

def computeMean(ar):
  return sum(ar) / float(len(ar))
  
def computeStdDev(ar, mean):
  s = 0
  for i in range(len(ar)):
    s += pow(ar[i] - mean, 2)
  return sqrt(s / float(len(ar) -1))


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


