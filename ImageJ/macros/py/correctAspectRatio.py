# correctAspectRatio.py
# Correct the aspect ratio for this calibrated image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-12-21  JRM 0.0.90  Initial

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ

bTestPath = False
homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
ePrjDir    = "QM15-02-16A9-Landry-Coltrain"
rPrjDir    = "QM15-02-16A-Landry-Coltrain"
sampID     = "qm-04587-LBT15-65-3-EK-FIB"
datDir     = "/Oxford/" + ePrjDir + "/reports/" + sampID
relIn      = datDir + "/tif/calib/"
relOut     = "/work/proj/" + rPrjDir + "/knitr/inc/png"
inDir      = edsDir + relIn
outDir     = homDir + relOut

imgName = "qm-04587-LBT15-65-3-EK-FIB-03s"

imgPath = inDir + imgName + ".tif"

if (bTestPath== True):
	print(inDir)
	print(imgPath)
else:
	theImp = IJ.openImage(imgPath)
	arImp = jmg.correctCalibAspectRatio(theImp, False)
	arImp.show()
	theImp.close()