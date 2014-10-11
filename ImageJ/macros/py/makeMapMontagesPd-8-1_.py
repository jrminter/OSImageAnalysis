# makeMapMontagesPd-8-1_.py
#
# Make montages from qm-04157-445005-248-Pd8-1-FIB-7kV-map
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-11  JRM 0.1.00  Test makeMontage in jmFijiGen

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ

homDir     = os.environ['HOME']
edsDir     = os.environ['EDS_ROOT']
relIn      = "/Oxford/QM14-04-03A-English/reports/248-Pd8-1-FIB-7kV-map/png"
relOut     = "/work/proj/QM14-04-03A-English/Sweave/inc/png"
outNamFull = "qm-04157-445005-248-Pd8-1-FIB-7kV-map-full.png"
outNamTmp  = "qm-04157-445005-248-Pd8-1-FIB-7kV-map-full.tif"
outNamCrop = "qm-04157-445005-248-Pd8-1-FIB-7kV-map-crop.png"

lNames  = ["2-OK","3-CuL","6-PK","7-PdL","8-AgL","9-ROI"]
#        sz   w-px  um
lCal = [1.45, 512, -6]


inDir  = edsDir + relIn
outDir = homDir + relOut
jmg.ensureDir(outDir)

outPth = outDir + "/" + outNamFull
impMontFull = jmg.makeMontage(lNames, 3, 2, inDir, lCal=lCal, sca=1.0)
impMontFull.show()
IJ.saveAs(impMontFull, "PNG", outPth)

# I know this is a hack...
# cache the full to recall at the end
tmpDir = jmg.makeTmpDir()
tmpPth = tmpDir + "/" + outNamTmp
IJ.saveAs(impMontFull, "TIF", tmpPth)

# now crop a ROI
#       x0  y0  w   h
lCr  = [200,30,200,220]
outPth = outDir + "/" + outNamCrop
impMontCrop = jmg.makeMontage(lNames, 3, 2, inDir, lCal=lCal, lCr=lCr, sca=1.0)
impMontCrop.show()
IJ.saveAs(impMontCrop, "PNG", outPth)

# now pull back the TIF to annotate
impMontFull = IJ.openImage(tmpPth)
impMontFull.show()

