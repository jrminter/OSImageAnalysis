# 02-montage-qm-nnnnn-sampleID-nnkV-map1
# Make montage from qm-nnnnn-sampleID-nnkV-map1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-07  JRM 0.1.00  Montage maps created with 01-Prep script
#                         this version tries to use standard directories
# 2014-11-07  JRM 0.1.10  Added a bTestPaths flag to test loading images 

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

bTestPaths = False
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
  impMontFull.show()
  IJ.saveAs(impMontFull, "PNG", outPth)


