# -*- coding: utf-8 -*-
#
# testCorPC.py
# 2014-01-11 J. R Minter
#
# Test the algorithm to measure and correct for probe current
# changes using Cu spectra as a proxy for probe current
# N.B. - Run this test from:
#        %GIT_HOME%/OSImageAnalysis/dtsa2/algTest/testCorPC

import dtsa2.jmGen as jmg
import os
import sys
import shutil

clean   = True  # clean up display
sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)
e0      = 12   # kV
wrkDist = 17.0 # mm

gitDir = os.environ['GIT_HOME']
edsRel = "/OSImageAnalysis/dtsa2/algTest/testCorPC"

#
# should not need to change below here...
#
wd = gitDir + edsRel + "/py"
os.chdir(wd)
pyrDir="testCorPC Results"

# start clean
DataManager.clearSpectrumList()


spcDir = gitDir + edsRel + "/spc"
unCuFi = spcDir + "/unCuSpc-12.spc"
rfCuFi = spcDir + "/rfCuSpc-12.spc"

rfCuSpc  = wrap(ept.SpectrumFile.open(rfCuFi)[0])
rfCuSpc  = jmg.updateCommonSpecProps(rfCuSpc, det, probeCur=1, e0=e0, wrkDist=wrkDist)
display(rfCuSpc)

unCuSpc  = wrap(ept.SpectrumFile.open(unCuFi)[0])
unCuSpc  = jmg.updateCommonSpecProps(unCuSpc, det, probeCur=1, e0=e0, wrkDist=wrkDist)
display(unCuSpc)

rpc = jmg.measProbeCurrentFromCu(unCuSpc, rfCuSpc, det, e0)
print(rpc["pcMu"])
print(rpc["pcSE"])

unCuSpc = jmg.updateCommonSpecProps(unCuSpc, det, probeCur=rpc["pcMu"], e0=e0, wrkDist=wrkDist)
display(unCuSpc)

rpc = jmg.measProbeCurrentFromCu(unCuSpc, rfCuSpc, det, e0)
print(rpc["pcMu"])
print(rpc["pcSE"])




if clean:
  clear()
  DataManager.removeSpectrum(rfCuSpc)
  DataManager.removeSpectrum(unCuSpc)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
