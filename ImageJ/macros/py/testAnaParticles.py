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
from java.awt import Color

from ij import IJ
from ij import ImagePlus
from ij.gui import Overlay, PointRoi
from ij.measure import ResultsTable, Measurements
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.frame import RoiManager
import jmFijiGen as jmg

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

def anaParticlesWatershed(imp, strThrMeth="method=Default white", minPx=10, minCirc=0.35, labCol=Color.white, linCol=Color.green, bDebug=False, sl=0.005):
  """anaParticlesWatershed(imp, strThrMeth="method=Default white", minPx=10, minCirc=0.35, labCol=Color.white, linCol=Color.green, bDebug=False, sl=0.005)
  A wrapper function to do particle analyis from an image after a watershed transformation and draw the detected
  features into the overlay of the original image.
  Inputs:
  imp        - the ImagePlus instance that we will process
  strThrMeth - a string specifying the threshold method
  minPx      - the minimum pixels to detect
  minCirc    - the minimum circularity to detect
  labCol     - the color for labels in the overlay (default white)
  linCol     - the color for line/stroke in the overlay (default green)
  bDebug     - a flag (default False) that, if true, keeps the work image open
  sl         - a time (default 0.005) to sleep when adding ROIs to not overload

  This adds the detected features to the overlay and returns the result table for
  processing for output.
  """
  title = imp.getTitle()
  shortTitle = imp.getShortTitle()
  
  typ = imp.getType()
  imp.setTitle(shortTitle)
  imp.show()
  IJ.run(imp,"Duplicate...", "title=work")
  wrk = IJ.getImage()
  # if this is a 16 bit image, convert to 8 bit prior to threshold
  if typ == ImagePlus.GRAY16:
    IJ.run(wrk, "Enhance Contrast", "saturated=0.35")
    IJ.run(wrk, "8-bit", "")
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
    # needed to put in sleep here on cruch to let this complete and not overrun buffer
    time.sleep(sl)
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
bVerbose = False

imgDir  = os.environ['IMG_ROOT']
rptDir  = os.environ['RPT_ROOT']
relImg  = "/key-test/AgX"
sampID  = "qm-03965-KJL-027"
nmPerPx = 1.213
minCirc = 0.5
minSize = 1000.0
maxSize = 10000.0

# set some strings
strScale = "distance=1 known=%.3f pixel=1 unit=nm global" % nmPerPx
strAna   = "size=%g-%g circularity=%.3f-1.00 exclude clear include add" % (minSize, maxSize, minCirc)

sImgPath = imgDir + relImg + "/" + sampID + "/dm3/" + sampID + "-01.dm3"
print(sImgPath)
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)
sRptCsvPath = sRptPath + sampID + ".csv"
sRptImgPath = sRptPath + "png/"
jmg.ensureDir(sRptImgPath)


orig = ImagePlus(sImgPath)
strName = os.path.basename(sImgPath)
strName = strName.split('.')[0]
orig.setTitle(strName)
orig.show()
# iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
# print(iZero)

# [ana, rt] = anaParticles(orig, minSize, maxSize, minCirc, bHeadless=bHeadless)
rt = jmg.anaParticlesWatershed(orig)
orig.show()
nMeas = rt.getCounter()
print("%d particles detected in image %d" % (nMeas,1) )
nCols = rt.getLastColumn()

if bVerbose == True:
  for j in range(nCols+1):
    print(rt.getColumnHeading(j))


print("Area     = %d" % rt.getColumnIndex("Area"))
print("Mean     = %d" % rt.getColumnIndex("Mean"))
print("Mode     = %d" % rt.getColumnIndex("Mode"))
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

outPth = sRptImgPath + strName + ".png"
# burn a scale bar and save the image
IJ.run(orig, "RGB Color", "")
IJ.run(orig, "Add Scale Bar", "width=100 height=6 font=28 color=Black location=[Lower Right] bold")
IJ.saveAs(orig, "PNG", outPth)

print("done")


