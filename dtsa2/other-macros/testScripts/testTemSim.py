# testTemSim.py
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
pyrDir = wd + "/testTemSim Results/"

det=findDetector("FEI CM20UT EDAX-RTEM")
e0    =   200 # kV
thMat =   100 # nm
thSub =    50 # nm
nTraj = 10000 # trajectories
lt    = 100   # sec
pc    = 1     # nA

# create materials
ago=epq.Material(epq.Composition([epq.Element.Ag, epq.Element.O],[0.930958,0.069042]), epq.ToSI.gPerCC(7.14))
c=epq.MaterialFactory.createPureElement(epq.Element.C)
spc = jmg.simMatlOnSubTEM(det, 200.0, ago, thMat, c, thSub, ["Ag2O","C"], nTraj, lt, pc)
display(spc)
brehm = jmg.simBrehmTEM(det, 200.0, ago, thMat, c, thSub, ["Ag2O","C"], nTraj, lt, pc)
display(brehm)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"