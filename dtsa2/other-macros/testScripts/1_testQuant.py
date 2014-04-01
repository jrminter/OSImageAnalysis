# 1_testQuant.py
#
# 2013-10-17 J. R. Minter 
# Test the TEM simulations in jmGen.py
#
import os
import shutil

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/1_testQuant Results/"

msaDir = git + "/OSImageAnalysis/dtsa2/msa/"
DataManager.clearSpectrumList()
sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)
pc      = 1.0
wrkDist = 17.2 # mm
vkV     = [15]

for e0 in vkV:
  cuStdFil = msaDir + "Cu-%g-Std.msa" % e0
  cuStdSpc = readSpectrum(cuStdFil, i=0, det=det)
  display(cuStdSpc)
  cuStd = {"Cu":cuStdSpc}
  
  cuUnkFil = msaDir + "Cu-%g-Unk.msa" % e0
  cuUnkSpc = readSpectrum(cuUnkFil, i=0, det=det)
  display(cuUnkSpc)
  
  a = quantify(cuUnkSpc, cuStd) #, preferred=trsCu)
  res = a.getComposition()
  dumpComps([res])


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
