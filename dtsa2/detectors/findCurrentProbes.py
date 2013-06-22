# findCurrentProbes.py
# this works

import os
import shutil
from gov.nist.microanalysis.EPQDatabase import Session

# Local system configuration options
# change as needed

gitHome=os.environ['GIT_HOME']
myHome=os.environ['HOME']
relDb ="/Database v2"
relDir="/OSImageAnalysis/dtsa2/detectors"
rptDir="/findCurrentProbes Results/"
dbDir=myHome+relDb
pyReptDir = gitHome + relDir + rptDir

# now we can do the work
probes=Session(dbDir).getElectronProbes()
print probes

# clean up cruft
shutil.rmtree(pyReptDir)
print "Done!"
