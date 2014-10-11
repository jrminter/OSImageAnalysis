# testSingleParticleDetector_.py
#
# Process the blob image and compute the maximum intrusion distance
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-30  JRM 0.1.00  Test the SingleParticleDetector plug-in with the
#                         blobs image

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
# imgPath = gitDir + relImg + "/blobs.gif"
imgPath = gitDir + relImg + "/model-agglomerates.tif"
print(imgPath)
rptPath = gitDir + relImg + "/"
# rptName = "blobs-size.csv"
rptName = "model-agglomerate-size.csv"
print(rptPath)

minArea = 10
maxArea = 999999
maxInt  = 2
doDraw  = 1

strSPD = "minarea=%g maxarea=%g maxintrusion=%g draw=%g path=%s report=%s" % (minArea, maxArea, maxInt,doDraw, rptPath, rptName )

raw = IJ.openImage(imgPath)
raw.show()

IJ.run("Auto Threshold", "method=Otsu white")
IJ.run("Make Binary")
IJ.run("Invert")
IJ.run("Single Particle Detector", strSPD)
