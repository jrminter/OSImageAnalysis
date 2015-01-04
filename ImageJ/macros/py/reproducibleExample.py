# reproducibleExample.py
#
# Test detection of large and small matte beads from an exemplar image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-18  JRM 0.1.00  Initial test am image of AgX grains
# 2015-01-03  JRM 0.2.00  Using some ideas
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij.gui import PointRoi
from ij.measure import ResultsTable, Measurements
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager

def anaParticles(imp, strMeth="method=Default white", minPx=10, minCirc=0.35, col="green", wid=1):
  imp.setTitle("original")
  IJ.run(imp,"Duplicate...", "title=work")
  wrk = IJ.getImage()
  IJ.run(wrk, "Threshold", strMeth)
  IJ.run(wrk, "Watershed", "")
  wrk.show()
  IJ.run(wrk, "Set Measurements...", "area mean modal min center perimeter bounding fit shape feret's display redirect=original decimal=3")
  # got this from IJ_Prefs.txt
  meas = 28379
  strAna = "size=%d-Infinity circularity=%g-1.00 show=[Overlay Outlines] display exclude clear include add" % (minPx, minCirc)
  IJ.run(wrk, "Analyze Particles...", strAna)
  rt = ResultsTable()
  pa = ParticleAnalyzer(0, meas, rt, minPx, float("inf"), minCirc, 1.0)
  pa.analyze(wrk);
  rt.createTableFromImage(wrk.getProcessor())
  rm = RoiManager.getInstance()
  ra = rm.getRoisAsArray()
  # Let's draw the particles into the overlay of the original
  for r in ra:
    imp.setRoi(r)
    strStroke = "  stroke=%s width=%g" % (col, wid)
    IJ.run(imp, "Properties... ", strStroke )
    IJ.run(imp, "Add Selection...", "")
  # let's put a PointRoi outside the image to get the overlays all the same color
  imp.setRoi(PointRoi(-10, -10))
  # clear the roi manager and return the results table
  rm.reset()
  return rt




IJ.run("Blobs (25K)")
ori = IJ.getImage()
myRT = anaParticles(ori)

myRT.show("Results")




  
  




