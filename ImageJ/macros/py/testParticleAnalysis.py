# testParticleAnalysis.py
#
# Test detection of large and small matte beads from an exemplar image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-18  JRM 0.1.00  Initial test am image of AgX grains
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
import jmFijiGen as jmg

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
strAna   = "size=%g-%g circularity=%.3f-1.00 show=[Overlay Outlines] display exclude clear include" % (minSize, maxSize, minCirc)

sImgPath = imgDir + relImg + "/" + sampID + "/"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)

query = sImgPath + "*.dm3"
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
  if i < 1:
    orig = ImagePlus(fi)
    strName = os.path.basename(fi)
    strName = strName.split('.')[0]
    orig.setTitle(strName)
    orig.show()
    iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
    print(iZero)
    imp = orig.duplicate()
    imp.setTitle("work")
    imp.show()
    IJ.run(imp, "Enhance Contrast", "saturated=0.35")
    IJ.run(imp, "8-bit", "")
    IJ.run(imp, "Threshold", "method=Default white")
    IJ.run(imp, "Watershed", "")
    imp.show()
    strSetMeas = "area modal min perimeter fit shape feret's redirect=%s decimal=3" % strName
    print(strSetMeas)
    IJ.run(imp, "Set Measurements...", strSetMeas)
    strAna = "size=%g-%g circularity=%.3f-1.00 show=[Overlay Outlines] display exclude clear include add" % (minSize, maxSize, minCirc)
    IJ.run(imp, "Analyze Particles...", strAna)
    rt = ResultsTable.getResultsTable()
    nMeas = rt.getCounter()
    print(nMeas)
    aSqNm = rt.getColumn(ResultsTable.AREA)
    ecdCol = rt.getFreeColumn("ECD.nm")
    print(ecdCol)
    rt.setHeading(ecdCol, "ECD.nm") 
    # ecdNm = []
    for j in range(len(aSqNm)):
      ecd = 2.0*sqrt(aSqNm[j]/3.1415926)
      rt.setValue(ecdCol, j, 17) 
      # rt.addValue(ecdCol, ecd)
      # ecdNm.append(ecd)
    rt.updateResults() 
    # gMode = rt.getColumn(ResultsTable.MODE) 
    if bClose:
      imp.changes = False
      imp.close()

    # Now draw particles into the original image
    rm = RoiManager.getInstance()
    ra = rm.getRoisAsArray()
    for r in ra:
      orig.setRoi(r)
      strStroke = "  stroke=%s width=%g" % (col, wid)
      IJ.run(orig, "Properties... ", strStroke )
      IJ.run(orig, "Add Selection...", "")
    
  i += 1 
