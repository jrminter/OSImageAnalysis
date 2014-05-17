# -*- coding: utf-8 -*-
#         1         2         3         4         5         6         7  
#123456789012345678901234567890123456789012345678901234567890123456789012
#
# createCustomSDD.py
# simulate a custom SDD
# J. R. Minter 2014-05-16 - initial version. Source in git repository
import os
import shutil
import java.io as jio
import math

git = os.environ['GIT_HOME']
edsDir = os.environ['EDS_ROOT']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros"
os.chdir(wd)
pyrDir = wd + "/createCustomSDD Results/"

dName = "cubeSDD"
nChan = 2048
eVpC  =   10.0
resMn =  128.0
toA   =   35.0   # take-off angle, deg
sToDd =   54.56  # sample to detector distance, mm
dA    =   80.00  # detector area, sq mm
opWD  =    5.00  # optimum working distance, mm
alLay =   10.0   # Al layer, nm

sR2 = math.sqrt(2.0)

refDet = findDetector("FEI FIB620 EDAX-RTEM")

# Create a new detector
dd=epq.Detector.EDSDetector.createSDDDetector(nChan, eVpC, resMn)
dd.getDetectorProperties().setName(dName)
dp=dd.getDetectorProperties().getProperties()
# Take-off -> 25 deg, sample-det distant -> 9.22 mm, optimal working distance-> 2.2 mm
dp.setDetectorPosition(toA*3.1415926/180.0, 0.0, sToDd*1e-03, opWD*1.0e-03)
# Set the detector to point at 225 degrees
dp.setArrayProperty(epq.SpectrumProperties.DetectorOrientation,[-1.0*sR2, -1.0*sR2, 0.0])
dp.setNumericProperty(epq.SpectrumProperties.Elevation, toA)
# Replace the gold layer with a Aluminum layer
dp.setNumericProperty(epq.SpectrumProperties.GoldLayer, 0.0)
dp.setNumericProperty(epq.SpectrumProperties.AluminumLayer, 10.0)
dp.setNumericProperty(epq.SpectrumProperties.DetectorArea, dA)
dp.setNumericProperty(epq.SpectrumProperties.MoxtekWindow, 3.3)

# sa = dp.getNumericProperty(epq.SpectrumProperties.SolidAngle)
dd = dp.getNumericProperty(epq.SpectrumProperties.DetectorDistance)
print(dd)



# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

