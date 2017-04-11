# testAnaKmag.py
#
# developing a KMAG analysis
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

import jmFijiGen as jmg


def anaKmag(imp, strThrMeth="method=Otsu white",
            minPx=10, minCirc=0.35, labCol=Color.white,
            linCol=Color.green, bDebug=False):
  """anaKmag(imp, strThrMeth="method=Default white",
             minPx=10, minCirc=0.35, labCol=Color.white,
             linCol=Color.green, bDebug=False)
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
  imp.show()
  IJ.run(imp,"Duplicate...", "title=work")
  wrk = IJ.getImage()
  IJ.run(wrk, "Median...", "radius=2")
  IJ.run(wrk, "Enhance Contrast", "saturated=0.05")
  wrk.setTitle(shortTitle + "-km")
  IJ.run(wrk, "Threshold", strThrMeth)
  IJ.run(wrk, "Fill Holes", "")
  IJ.run(wrk, "Properties...", "channels=1 slices=1 frames=1 unit=px pixel_width=1 pixel_height=1 voxel_depth=1")
  IJ.run(wrk, "Set Measurements...", "area centroid center perimeter shape display redirect=None decimal=3")
  IJ. run(wrk, "Analyze Particles...", "display exclude clear add");
  
  return wrk


IJ.run("Close All");
closeRW = False
IJ.open("C:\\Data\\images\\key-test\\KMAG\\qm-05227-KMAG-96-19-08.tif");
ori = IJ.getImage()
kmi = anaKmag(ori)
kmi.show()




  
  




