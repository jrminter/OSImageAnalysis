# renameProbes.py
# rename non default probes to standard names
# Doesn't work yet
# 

import os
import shutil
from gov.nist.microanalysis.EPQDatabase import Session

# change as needed
curNames=["FEI CM20UT D692", "NIST JXA-8500F", "FEI Dual Beam 620"]
newNames=["FEICM20UT", "JXA3500F", "FEI620"]

gitHome=os.environ['GIT_HOME']
myHome=os.environ['HOME']
relDb ="/Database v2"
relDir="/OSImageAnalysis/dtsa2/detectors"
rptDir="/renameProbes Results/"
dbDir=myHome+relDb
pyReptDir = gitHome + relDir + rptDir

# now we do the real work
probes=Session(dbDir).getElectronProbes()
for i in range(len(curNames)):
  probe=Session(dbDir).getElectronProbe(curNames[i])
  probe.setName(newNames[i])

# clean up cruft
shutil.rmtree(pyReptDir)
print "Done!"