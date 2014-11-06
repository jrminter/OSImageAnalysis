# 02-montage-qm-04219-49G003-188-7kV-map-1
# Make montage from qm-04219-49G003-188-7kV-map-1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-06  JRM 0.1.00  Test makeMontage in jmFijiGen

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
relIn      = "/Oxford/QM14-04-06B-Wansha/reports/qm-04219-493004-188/qm-04219-493004-188-7kV-map1/work"
relOut     = "/work/proj/QM14-04-06B-Wansha/Sweave/inc/png"
outNamFull = "qm-04219-49G003-188-7kV-map-1.png"

lNames  = ["N-K","O-K","Cu-L", "P-K", "Na-K","Cl-K", "Pd-L", "Ag-L", "ROI"]

#        sz   w-px  um
lCal = [116., 1023, -6]


inDir  = edsDir + relIn
outDir = homDir + relOut
jmg.ensureDir(outDir)

outPth = outDir + "/" + outNamFull
impMontFull = jmg.makeMontage(lNames, 3, 3, inDir, lCal=lCal, sca=1.0)
impMontFull.show()
IJ.saveAs(impMontFull, "PNG", outPth)


