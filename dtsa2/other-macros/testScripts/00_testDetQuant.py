# 00_testDetQuant.py
#
# 2014-04-01 J. R. Minter 
# Test quantify with spectra matched to the detector
#
import os
import shutil
import java.io as jio
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/00_testDetQuant Results/"

DataManager.clearSpectrumList()
spcDir = git + "/OSImageAnalysis/dtsa2/spc/"

sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)
pc      = 1.0
wrkDist = 17.2 # mm
vkV     = [15]

for e0 in vkV:
  cuFil = spcDir + "Cu-%g-1.spc" % e0
  raw = readSpectrum(cuFil, i=0, det=None)
  print(raw.getChannelCount())
  cuStdSpc = jmg.matchDet(raw, det)
  # try remap to see if it picks up calibration
  cuStdSpc = cuStdSpc.remap(det)
  cuStdSpc.setAsStandard(epq.Composition(epq.Element.Cu))
  cuStdSpc.rename("CuStd")  
  # set up the standard
  print(cuStdSpc.getChannelCount())
  display(cuStdSpc)
  cuStd = {"Cu":cuStdSpc}
  
  cuFil = spcDir + "Cu-%g-2.spc" % e0
  raw = readSpectrum(cuFil, i=0, det=None)
  print(raw.getChannelCount())
  cuSpc = jmg.matchDet(raw, det)
  # try remap to see if it picks up calibration
  cuSpc = cuSpc.remap(det)
  cuSpc.rename("CuUnk")
  print(cuSpc.getChannelCount())
  display(cuSpc)
  
  a = quantify(cuSpc, cuStd) #, preferred=trsCu)
  res = a.getComposition()
  dumpComps([res])



# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
