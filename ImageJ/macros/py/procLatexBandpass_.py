# procLatexbBndpass_.py
#
# Process a Latex image and compute the mean and std dev of the ECD (in px)
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-28  JRM 0.1.00  Translated from .ijm file and updated
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
rptPath = gitDir + relImg + "/latex-size.csv"
print(rptPath)

raw = IJ.openImage(imgPath)
nmPerPx = 2.02
raw = jmg.calibImageDirect(raw, nmPerPx, units=-9)
raw.show()
IJ.run("Bandpass Filter...", "filter_large=40 filter_small=1 suppress=None tolerance=5 autoscale saturate");


