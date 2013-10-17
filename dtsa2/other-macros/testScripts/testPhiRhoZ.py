# testPhiRhoZ.py
#
# 2013-10-17 J. R. Minter 
# Test the TEM simulations in jmGen.py
#
import os
import shutil
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/testPhiRhoZ Results/"

e0     =  25
nSteps = 200
cu     = material("Cu", density=8.96)
det    = findDetector("FEI FIB620 EDAX-RTEM")
jmg.compPhiRhoZ(cu, det, e0, nSteps, alg=epq.XPP1991(), base="xpp-prz", outdir="c:/temp/")

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"