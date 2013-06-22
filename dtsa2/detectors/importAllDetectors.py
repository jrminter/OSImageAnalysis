# importAllDetectors.py
#
# J. R. Minter Version of 2013-06-22
# delete all existing detectors and read all the files
# and import detector from each file
#
# Doesn't work yet. Do not use.
# Now a work in progress - Version 0.01
import os
import sys
import shutil
import fnmatch
from java.io import File
from gov.nist.microanalysis.EPQDatabase import Session

# Local system configuration options
gitHome=os.environ['GIT_HOME']
myHome=os.environ['HOME']
relDb ="/Database v2"
relDir="/OSImageAnalysis/dtsa2/detectors"
rptDir="/importAllDetectors Results/"
detDir=gitHome + relDir
dbDir=myHome+relDb
pyReptDir = gitHome + relDir + rptDir

probes =Session(dbDir).getElectronProbes()
print probes
print len(probes)
# find and process all detector XML files
for file in os.listdir(detDir):
  if fnmatch.fnmatch(file, '*.xdet'):
    # it is a detector file
    theFile=detDir + '/' + file
    # print theFile
    myFile = File(theFile)
    dd=epq.Detector.EDSDetector.readXML(myFile)
    dp=dd.getDetectorProperties().getProperties()
    detName=dd.getName()
    print detName
    # find the space
    ind=detName.index(" ")
    inst=detName[0:ind]
    epq.Detector.ElectronProbe(inst)
    print inst


# clean up cruft
shutil.rmtree(pyReptDir)
print "Done!"



