# -*- coding: utf-8 -*-
#
# anaSiBeamCal.py
# 
#   Date      Who  Comments
# ==========  ===  =========================================================================
# 2014-09-23  JRM  Measure the probe current with DTSA from Si Std

import os
import sys
import glob
import math
import shutil
import time
import java.io as jio
import dtsa2.jmGen as jmg

edsDir = os.environ['EDS_ROOT']
relDir = "/Oxford/QM14-04-05A-Bauer"
wd = edsDir + relDir + "/reports/py"
os.chdir(wd)
pyrDir="./anaSiBeamCal Results"
datDir = edsDir + relDir + "/reports"
spcDir = datDir + "/Si-pt6-5eV-2K"
rptDir = datDir + "/csv"
jmg.ensureDir(rptDir)
rptFil = rptDir + "/probeCurrent.csv"

sDet    = "Oxford p6 05eV 2K"
det     = findDetector(sDet)
wrkDist = 5.0 # mm

spcBas = datDir + "/msa"
jmg.ensureDir(spcBas)

lNames  = ["Si-7kV-Beam-Calib"]


lPc = []
iCnt = 0

DataManager.clearSpectrumList()
for name in lNames:
  spcFil = spcBas + "/%s.txt" % name
  print(spcFil)
  spc = readSpectrum(spcFil, i=0, det=det)
  lt = spc.liveTime()
  sp = spc.getProperties()
  e0 = sp.getNumericProperty(epq.SpectrumProperties.BeamEnergy)
  sp.setCompositionProperty(epq.SpectrumProperties.StandardComposition, epq.Composition(epq.Element.Si))
  print(e0)
  a = fitSpectrum(spc, nIter=5)
  siChar = wrap(a["Char"])
  siChar.rename("Fit Si Char at %g kV" % e0)
  display(siChar)
  int = siChar.peakIntegral(1629, 1931)
  piMu = round((int.doubleValue()/lt), 1)
  print(piMu)
  cpsPerNa = jmg.getSirionSiCpsPerNa(e0)
  pc = round(piMu/cpsPerNa, 3)
  print(pc)
  lPc.append(pc)
  
# write out results
f=open(rptFil, 'w')
strLine = 'name,pc.na\n'
f.write(strLine)
  
for i in range(len(lNames)):
  strLine = "%s" % lNames[i] + ","
  strLine = strLine + "%.3f" % lPc[i]  + "\n"
  f.write(strLine)

f.close()

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

