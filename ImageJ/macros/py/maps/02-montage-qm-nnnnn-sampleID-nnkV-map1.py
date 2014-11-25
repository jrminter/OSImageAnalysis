# 02-montage-qm-nnnnn-sampleID-nnkV-map1
# Make montage from qm-nnnnn-sampleID-nnkV-map1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-07  JRM 0.1.00  Montage maps created with 01-Prep script
#                         this version tries to use standard directories
# 2014-11-07  JRM 0.1.10  Added a bTestPaths flag to test loading images
# 2014-11-10  JRM 0.1.11  Be sure to set title 
# 2014-11-13  JRM 0.1.12  Option to scale
# 2014-11-24  JRM 0.1.13  This adds annotations and scale bars

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ
from java.awt import Color

# check that paths are correct by loading ROI image
bTestPaths = False
# scale the image by scaFac
bScale     = True
scaFac     = 0.5

# For scale bar
# loc for scale bar. if sbPtX=None will be lower right
sbPtX  = 1400
sbPtY  =  940
sbW    =   50  # units from cal
sbH    =    6  # px
sbFont =   24  # points
sbCol  =  "White"  # color

homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
ePrjDir    = "QM14-nn-nnA-Client"
# this is different because ePrjDir often has a suffix because there
# are multiple AZtec projects for the same job. Data sets get big
# and unwieldy...
rPrjDir    = "QM14-nn-nnA-Client"
sampID     = "qm-nnnnn-sampleID"
mapID      = "nnkV-map1" 

# map fills row-by row left to right
lName = ["C-K", "N-K","O-K","Cu-L", "P-K", "Cl-K", "Pd-L", "Ag-L", "ROI"]
# names for Annotations
lAnn  = ["C"  , "N"  ,"O"  ,  "Cu",   "P",   "Cl",   "Pd",   "Ag", "ROI"]
nCol = 3
nRow = 3
#        sz   w-px  um
lCal = [193., 1024, -6]
  
datDir     = "/Oxford/" + ePrjDir + "/reports/" + sampID + "/" + sampID + "-" + mapID
relIn      = datDir + "/work"

relOut     = "/work/proj/" + rPrjDir + "/Sweave/inc/png"
outNamFull = sampID + "-" + mapID + ".png"

inDir  = edsDir + relIn
outDir = homDir + relOut
outPth = outDir + "/" + outNamFull

if bTestPaths == True:
  # print the directories and try loading the ROI image
  print(inDir)
  strImg = inDir + "/ROI.png"
  imp = IJ.openImage(strImg)
  if imp == None:
    print("Error loading ROI.png")
  else:
    imp.show()
  print(outPth)
else:
  jmg.ensureDir(outDir)
  impMontFull = jmg.makeMontage(lName, nCol, nRow, inDir, lCal=lCal, sca=1.0)
  if bScale:
    newW = round(scaFac * impMontFull.getWidth())
    newH = round(scaFac * impMontFull.getHeight())
    newN = sampID + "-" + mapID
    strSca = "x=%g y=%g width=%d height=%d interpolation=Bicubic average create title=%s" % (scaFac, scaFac, newW, newH, newN)

    IJ.run(impMontFull, "Scale...", strSca )
    impMontFull.changes=False
    impMontFull.close()
    impOut = IJ.getImage()
  else:
    impOut = impMontFull
  inImg = impOut 
  # Note: this returns a duplicate 
  impOut = jmg.labelMontage(impOut, lAnn, nCol, nRow, w0=12, h0=2, font=24, col=Color.WHITE)
  impOut.setTitle(sampID + "-" + mapID)
  
  # show the annotated image
  impOut.show()
  # burn a scale bar
  if sbPtX == None:
    strSB = "width=%g height=%g font=%g color=%s location=[Lower Right] bold" % (sbW, sbH, sbFont, sbCol )
  else:
    IJ.makePoint(sbPtX, sbPtY)
    strSB = "width=%g height=%g font=%g color=%s location=[At Selection] bold" % (sbW, sbH, sbFont, sbCol )
  # first burn a scale bar in the original image to make sure changes are written
  IJ.run(inImg, "Add Scale Bar", strSB)
  # close the original
  inImg.changes = False
  inImg.close()

  # now burn the scale bar we really want...
  IJ.run(impOut, "Add Scale Bar", strSB)
  # impOut.setTitle(sampID + "-" + mapID)
  IJ.makePoint(-10, -10)
  impOut.updateAndRepaintWindow()
  
  IJ.saveAs(impOut, "PNG", outPth)
