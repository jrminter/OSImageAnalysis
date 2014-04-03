# 3_testCalDet.py
#
# 2014-04-03 J. R. Minter 
# Test calibrating a detector from a script
#
import os
import shutil
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/3_testCalDet Results/"

spcDir = git + "/OSImageAnalysis/dtsa2/detectors/"
DataManager.clearSpectrumList()
sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)

spcFil = spcDir + "FIB620-Cu-25-1.spc"
spc = wrap(ept.SpectrumFile.open(spcFil)[0])
display(spc)
print(spc.getChannelCount())

mat = jmg.matchDet(spc, det)
cu = material("Cu", density=8.96)
mat.setAsStandard(cu)
display(mat)
print(mat.getChannelCount())

sf = epq.SpectrumFitter8(det, cu, mat)
# print(dir(sf))
rois = sf.getROIS()
print(rois)

# print(epq.FromSI.keV(rois.highEnergy()-rois.lowEnergy())/3.0)

pr = mat.getProperties()
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
# sf.recompute(20.0, 0.5)
# fitSpectrum = sf.getBestFit()
# display(fitSpectrum)




# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
