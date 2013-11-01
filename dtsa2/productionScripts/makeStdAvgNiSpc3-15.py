# -*- coding: utf-8 -*-
# makeStdAvgNiSpc3-15.py
# 2013-11-01 J. R. Minter
# written to average 3 Ni spectra Ni stds for qm-03900


import os
import sys
import glob
import shutil
import time

edsDir = os.environ['EDS_ROOT']
relDir = "/CuNiSpc/qm-03900-180nmNiOnCuGrid"
wd = edsDir + relDir + "/py"
os.chdir(wd)
pyrDir="./makeStdAvgNiSpc3-15 Results"

def avgThreeSpectra(dir, names, resName="Avg"):
  sPath = dir+names[0]
  s0  = wrap(ept.SpectrumFile.open(sPath)[0])
  sPath = dir+names[1]
  s1  = wrap(ept.SpectrumFile.open(sPath)[0])
  sPath = dir+names[2]
  s2  = wrap(ept.SpectrumFile.open(sPath)[0])
  sum=s0+s1+s2
  avg=sum.subSample(100)
  avg.rename(resName)
  return avg
  
  
vkV = [15]

for e0 in vkV:
  disName='Ni Std %gkV' % e0

  sp1 = 'Ni-%g-1.spc' % e0
  sp2 = 'Ni-%g-2.spc' % e0
  sp3 = 'Ni-%g-3.spc' % e0
  
  myDir = edsDir + relDir + '/spc/stds/'
  spcNames=[sp1, sp2, sp3]
  theAvg = avgThreeSpectra(myDir, spcNames, resName=disName)
  display(theAvg)
  outDir = edsDir + relDir + '/msa/std/%gkV/' % e0
  outFil = outDir + 'Ni.msa'
  a = glob.glob(outFil)
  if (len(a) > 0):
    os.remove(a[0])
  fos=jio.FileOutputStream(outFil)
  ept.WriteSpectrumAsEMSA1_0.write(theAvg,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
  fos.close()
  

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

