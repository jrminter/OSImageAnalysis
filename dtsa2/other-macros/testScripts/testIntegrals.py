# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-26
# testIntegrals.py

import os
import shutil
import dtsa2 as dt2
import dtsa2.jmGen as jmg

wrkDist = 17.1 # mm
sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)

git = os.environ['GIT_HOME']
eds = os.environ['EDS_ROOT']
spcDir = eds + "/CuPdSpc/qm-04062-3C3006/spc/stds/"

# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/testIntegrals Results/"


# start clean
DataManager.clearSpectrumList()

spcFil = spcDir + "Cu-15-1.spc"
cuSpc1  = wrap(ept.SpectrumFile.open(spcFil)[0])
liveTim = cuSpc1.getProperties().getNumericProperty(epq.SpectrumProperties.LiveTime)
cuSpc1  = jmg.updateCommonSpecProps(cuSpc1, det, liveTime=liveTim, probeCur=1, wrkDist=wrkDist)
display(cuSpc1)

spcFil = spcDir + "Cu-15-2.spc"
cuSpc2  = wrap(ept.SpectrumFile.open(spcFil)[0])
liveTim = cuSpc2.getProperties().getNumericProperty(epq.SpectrumProperties.LiveTime)
cuSpc2  = jmg.updateCommonSpecProps(cuSpc2, det, liveTime=liveTim, probeCur=1, wrkDist=wrkDist)
display(cuSpc2)

spcFil = spcDir + "Cu-15-3.spc"
cuSpc3  = wrap(ept.SpectrumFile.open(spcFil)[0])
liveTim = cuSpc3.getProperties().getNumericProperty(epq.SpectrumProperties.LiveTime)
cuSpc3  = jmg.updateCommonSpecProps(cuSpc3, det, liveTime=liveTim, probeCur=1, wrkDist=wrkDist)
display(cuSpc3)

eL = jmg.getLalphaEnergy("Cu")
eK = jmg.getKalphaEnergy("Cu")
iL = jmg.compPeakIntegral(cuSpc1, eL, 135, digits=1)
print(iL)
iK = jmg.compPeakIntegral(cuSpc1, eK, 135, digits=1)
print(iK)
a = jmg.sumCounts(cuSpc1, 0, 1500)
print(a)

iL = jmg.compPeakIntegral(cuSpc2, eL, 135, digits=1)
print(iL)
iK = jmg.compPeakIntegral(cuSpc2, eK, 135, digits=1)
print(iK)
a = jmg.sumCounts(cuSpc2, 0, 1500)
print(a)

iL = jmg.compPeakIntegral(cuSpc3, eL, 135, digits=1)
print(iL)
iK = jmg.compPeakIntegral(cuSpc3, eK, 135, digits=1)
print(iK)
a = jmg.sumCounts(cuSpc3, 0, 1500)
print(a)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"



