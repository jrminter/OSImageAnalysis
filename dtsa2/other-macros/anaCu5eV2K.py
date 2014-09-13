# -*- coding: utf-8 -*-
#
# anaCu5eV2K.py
# 
#   Date      Who  Comments
# ==========  ===  =========================================================================
# 2014-09-12  JRM  Initial prototype for analysis analysis of Cu-L cps/nA

import os
import sys
import glob
import math
import shutil
import time
import java.io as jio
import dtsa2.jmGen as jmg

edsDir = os.environ['EDS_ROOT']
relDir = "/Oxford/2014-09-12-Cu-Si"
wd = edsDir + relDir + "/py"
os.chdir(wd)
pyrDir="./anaCu5eV2K Results"
datDir = edsDir + relDir + "/reports"
spcDir = datDir + "/Cu-pt6-5eV-2K"
rptDir = datDir + "/csv"
jmg.ensureDir(rptDir)
rptFil = rptDir + "/cps-per-nA-CuL-Oxford-p6-05eV-2K.csv"

sDet    = "Oxford p6 05eV 2K"
det     = findDetector(sDet)
wrkDist = 5.0 # mm

stdBas = datDir + "/stds"
jmg.ensureDir(stdBas)
stdBas = stdBas + "/" + sDet
jmg.ensureDir(stdBas)



lE0  = [5   , 7   , 10   , 15   , 20   , 30]
lPc  = [0.46, 0.60,  0.72,  0.83,  0.78,  0.78]
pcSd = 0.01

lCpsPerNaMu = []
lCpsPerNaSd = []
iCnt        = 0

DataManager.clearSpectrumList()
for i in range(len(lE0)):
  e0 = lE0[i]
  stdDir = "%s/%dkV" % (stdBas, e0)
  jmg.ensureDir(stdDir)
  pc = lPc[i]
  pcRSD = pcSd/pc
  cuFil = spcDir + "/Cu-%gkV-pt6-5eV-2K.txt" % e0
  cuStdSpc = readSpectrum(cuFil, i=0, det=det)
  lt = cuStdSpc.liveTime()
  sp = cuStdSpc.getProperties()
  sp.setCompositionProperty(epq.SpectrumProperties.StandardComposition, epq.Composition(epq.Element.Cu))
  sp.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
  sp.setTextProperty(epq.SpectrumProperties.InstrumentOperator, "John Minter")
  sp.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, "Cu")
  sp.setTextProperty(epq.SpectrumProperties.SpectrumComment, "Cu")
  stdFil = stdDir + "/Cu.msa"
  # write the standard
  a = glob.glob(stdFil)
  if (len(a) > 0):
    os.remove(a[0])
  fos=jio.FileOutputStream(stdFil)
  ept.WriteSpectrumAsEMSA1_0.write(cuStdSpc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
  fos.close()
  # display(cuStdSpc)
  a = fitSpectrum(cuStdSpc, nIter=5)
  # print(a)
  # print("fit %s" % cuFil)
  # display(a["Fit"])
  cuChar = wrap(a["Char"])
  cuChar.rename("Fit Cu Char at %g kV" % e0)
  display(cuChar)
  int = cuChar.peakIntegral(735, 1079)
  piMu = round((int.doubleValue()/lt), 1)
  piSd = round((int.uncertainty()/lt), 1)
  piRsd = int.uncertainty() / int.doubleValue()
  # print(piRsd)
  # print(piMu, piSd)
  piPerNaMu = piMu / pc
  lCpsPerNaMu.append(piPerNaMu)
  # add the uncertainties in quadrature
  piPerNaSd = piPerNaMu * math.sqrt(piRsd*piRsd + pcRSD*pcRSD)
  lCpsPerNaSd.append(piPerNaSd)
  
# write out results
f=open(rptFil, 'w')
strLine = 'e0,CuL.cps.per.na.mu,CuL.cps.per.na.sd\n'
f.write(strLine)

for i in range(len(lE0)):
  strLine = "%d" % lE0[i] + ","
  strLine = strLine + "%.1f" % lCpsPerNaMu[i]  + ","
  strLine = strLine + "%.1f" % lCpsPerNaSd[i]  + "\n"
  f.write(strLine)

f.close()



# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

