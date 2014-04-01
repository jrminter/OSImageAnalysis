# 2_testMatchDet.py
#
# 2014-04-01 J. R. Minter 
# Test the matchDet function in jmGen.py
#
import os
import shutil
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/2_testMatchDet Results/"

spcDir = git + "/OSImageAnalysis/dtsa2/spc/"
DataManager.clearSpectrumList()
sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)

spcFil = spcDir + "Cu-15-1.spc"
spc = readSpectrum(spcFil, i=0, det=None)
display(spc)
print(spc.getChannelCount())

mat = jmg.matchDet(spc, det)
display(mat)
print(mat.getChannelCount())

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
