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
zOff  =  100.0

def createTempDetector(rDet, dName, nChan, eVpC, zOff, resMn):
  """createTempDetector(rDet, dName, nChan, eVpC, zOff, resMn)
  Create a temporary detector with name (dName) with (nChan) channels and
  (eVpC) ev/ch and (zOff) zero offset with resMn resolution"""
  
  # define a couple of helper functions...
  def copyNumericProp(nD, oD, prop):
    """copyNumericProp(nD, oD, prop)
    Copy numeric prop from old detector (oD) to new detector (nD)"""
    odp = oD.getDetectorProperties().getProperties()
    ndp = nD.getDetectorProperties().getProperties()
    np  = odp.getNumericProperty(prop)
    ndp.setNumericProperty(prop, np)

  def copyArrayProp(nD, oD, prop):
    """copyArrayProp(nD, oD, prop)
    Copy array prop from old detector (oD) to new detector (nD)"""
    odp = oD.getDetectorProperties().getProperties()
    ndp = nD.getDetectorProperties().getProperties()
    np  = odp.getArrayProperty(prop)
    ndp.setArrayProperty(prop, np)


  # Create a new temporary detector
  tD=epq.Detector.EDSDetector.createSDDDetector(nChan, eVpC, resMn)
  tD.getDetectorProperties().setName(dName)
  tdp = tD.getDetectorProperties().getProperties()
  tdp.setNumericProperty(epq.SpectrumProperties.EnergyOffset, zOff)
  
  copyArrayProp(tD, rDet, epq.SpectrumProperties.DetectorPosition)
  copyArrayProp(tD, rDet, epq.SpectrumProperties.DetectorOrientation)

  copyNumericProp(tD, rDet, epq.SpectrumProperties.Elevation)
  copyNumericProp(tD, rDet, epq.SpectrumProperties.AluminumLayer)
  copyNumericProp(tD, rDet, epq.SpectrumProperties.DetectorArea)
  copyNumericProp(tD, rDet, epq.SpectrumProperties.DetectorDistance)
  copyNumericProp(tD, rDet, epq.SpectrumProperties.SolidAngle)
  copyNumericProp(tD, rDet, epq.SpectrumProperties.MoxtekWindow)
  
  return tD

# start clean
DataManager.clearSpectrumList()

rD = findDetector("Oxford XMaxN 80")
theTD = createTempDetector(rD, dName, nChan, eVpC, zOff, resMn)
print(theTD.toString())
dp = theTD.getDetectorProperties().getProperties()
dd = dp.getNumericProperty(epq.SpectrumProperties.DetectorDistance)
print(dd)
rDp = rD.getDetectorProperties().getProperties()
dd = rDp.getNumericProperty(epq.SpectrumProperties.DetectorDistance)
print(dd)

# let's use it to do something
cu  = material("Cu", density=8.96)
sim = simulate(cu, det=theTD, keV=20, dose=100, withPoisson=True)
display(sim)

sf = epq.SpectrumFitter8(theTD, cu, sim)
# print(dir(sf))
rois = sf.getROIS()
print(rois)

# print(epq.FromSI.keV(rois.highEnergy()-rois.lowEnergy())/3.0)

pr = sim.getProperties()
# print(dir(pr))
props = pr.getDetector().getCalibration().getProperties()
# print(props)
coeffs = [props.getNumericWithDefault(epq.SpectrumProperties.EnergyOffset, 0.0),
props.getNumericWithDefault(epq.SpectrumProperties.EnergyScale, 10.0),
props.getNumericWithDefault(epq.SpectrumProperties.EnergyQuadratic, 0.0),
0.0,
0.0]
print(coeffs)
sf.setEnergyScale(epq.SpectrumFitter8.EnergyScaleFunction(coeffs, 6))
sf.setResolution(epq.SpectrumFitter8.FanoNoiseWidth(6.0));
sf.setMultiLineset(sf.buildWeighted(rois));
sf.compute()
fitSpectrum = sf.getBestFit()
display(fitSpectrum)

els = sf.getElementSpectrum(epq.Element.Cu)
display(els)

bss = sf.getBremsstrahlungSpectrum()
display(bss)

bfp = sf.getBestFitParameters()
print(bfp)


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

