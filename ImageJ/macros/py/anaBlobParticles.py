# anaBlobParticles.py
#
# A reproducible example of analyzing particles after a watershed transform
# and drawing the features into the original image window. This uses helper
# functions to draw the ROI
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-03  JRM 0.1.00  Initial test on blob image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from java.awt import Color
from ij import IJ
from ij import ImagePlus
from ij.gui import Overlay, PointRoi
from ij.measure import ResultsTable, Measurements
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager

def addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.white):
  """addRoiToOverlay(imp, roi, labCol=Color.white, linCol=Color.white)
  A convenience function to draw a ROI into the overlay of an ImagePlus. This is useful for
  situations where ROIs are computed from a highly processed image and tha analyst wants to
  draw them into the overlay of the original image (e.g. particle analysis after a 
  watershed separation. Adapted from addToOverlay() from Analyzer.java
  Inputs:
  imp    - the ImagePlus instance into which we draw the ROI
  roi    - the ROI to draw
  labCol - the color or the label (default white)
  linCol - the color of the stroke/line (default white)
  Returns
  imp    - the ImagePlus with the updated overlay"""
  roi.setIgnoreClipRect(True)
  ovl = imp.getOverlay()
  if ovl == None:
    ovl = Overlay()
  ovl.drawNames(True)
  ovl.setStrokeColor(linCol)
  ovl.setLabelColor(labCol);
  ovl.drawBackgrounds(False);
  ovl.add(roi)
  imp.setOverlay(ovl)
  return imp

def anaParticlesWatershed(imp, strThrMeth="method=Default white", minPx=10, minCirc=0.35, labCol=Color.white, linCol=Color.green, bDebug=False):
  """anaParticlesWatershed(imp, strThrMeth="method=Default white", minPx=10, minCirc=0.35, labCol=Color.white, linCol=Color.green, bDebug=False)
  A wrapper function to do particle analyis from an image after a watershed transformation and draw the detected
  features into the overlay of the original image.
  Inputs:
  imp        - the ImagePlus instance that we will process
  strThrMeth - a string specifying the threshold method
  minPx      - the minimum pixels to detect
  minCirc    - the minimum circularity to detect
  labCol     - the color for labels in the overlay (default white)
  linCol     - the color for line/stroke in the overlay (default green)
  bDebug     - a flag (default False) that, if true, keeps the work image opem

  This adds the detected features to the overlay and returns the result table for
  processing for output.
  """
  title = imp.getTitle()
  shortTitle = imp.getShortTitle()
  imp.setTitle(shortTitle)
  IJ.run(imp,"Duplicate...", "title=work")
  wrk = IJ.getImage()
  IJ.run(wrk, "Threshold", strThrMeth)
  IJ.run(wrk, "Watershed", "")
  wrk.show()
  strMeas = "area mean modal min center perimeter bounding fit shape feret's display redirect=%s decimal=3" % shortTitle
  IJ.run(wrk, "Set Measurements...", strMeas)
  strAna = "size=%d-Infinity circularity=%g-1.00  exclude clear include add" % (minPx, minCirc)
  IJ.run(wrk, "Analyze Particles...", strAna)
  rt = ResultsTable().getResultsTable()
  rm = RoiManager.getInstance()
  ra = rm.getRoisAsArray()
  # Let's draw the particles into the overlay of the original
  i=0
  for r in ra:
    i += 1
    rLab = "%d" % i
    r.setName(rLab)
    imp = addRoiToOverlay(imp, r, labCol=labCol, linCol=linCol)
  # let's put a PointRoi outside the image to get the overlays all the same color
  r = PointRoi(-10, -10)
  imp = addRoiToOverlay(imp, r, labCol=labCol, linCol=linCol)
  # clear the roi manager and return the results table
  rm.reset()
  rm.close()
  if bDebug == False:
    wrk.changes = False
    wrk.close()
  imp.setTitle(title)
  return rt



closeRW = False

IJ.run("Blobs (25K)")
ori = IJ.getImage()
myRT = anaParticlesWatershed(ori)

myRT.show("Results")

if closeRW:
  myRT.getResultsWindow().close(False)
else:
  myRT.show("Results")




  
  




