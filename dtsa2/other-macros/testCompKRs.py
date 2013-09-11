# testCompKRs.py

# testing a generic K-Ratio function
import os
import sys
import shutil

e0      = 15    # kV
dose    = 150   # nA*sec
maxCh   = 1200  # ending channel
edsDet  = "FEI FIB620 EDAX-RTEM"
det     = findDetector(edsDet)

home    = os.environ['HOME']
gitDir  = os.environ['GIT_HOME']
relGit  = "/OSImageAnalysis/dtsa2/other-macros"
relDir  = "/work/"
relStd  = "proj/trThickNiOnCu/dat/dtsa-sim/CorBulk/15kV/"
relUnk  = "proj/trThickNiOnCu/dat/dtsa-sim/StrataGemNiCu/"
relPy   = "/testCompKRs Results/"
rptPy   = gitDir + relGit + relPy
stdDir  = home+relDir+relStd
unkDir  = home+relDir+relUnk

trs = [epq.XRayTransitionSet(epq.Element.C, epq.XRayTransitionSet.K_FAMILY),
epq.XRayTransitionSet(epq.Element.O, epq.XRayTransitionSet.K_FAMILY),
epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.L_FAMILY),
epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.K_FAMILY),
epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.L_FAMILY),
epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.K_FAMILY)]
        
cFile = stdDir + "C-sim.msa"
cSpc = ept.SpectrumFile.open(cFile)[0]
cSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ws = wrap(cSpc)
cSpc = cropSpec(ws, end=maxCh)
cSpc = setKeySimSpcProps(cSpc, e0, dose)

oFile = stdDir + "B2O3-sim.msa"
oSpc = ept.SpectrumFile.open(oFile)[0]
oSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ws = wrap(oSpc)
oSpc = cropSpec(ws, end=maxCh)
oSpc = setKeySimSpcProps(oSpc, e0, dose)

niFile = stdDir + "Ni-sim.msa"
niSpc = ept.SpectrumFile.open(niFile)[0]
niSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ws = wrap(niSpc)
niSpc = cropSpec(ws, end=maxCh)
niSpc = setKeySimSpcProps(niSpc, e0, dose)

cuFile = stdDir + "Cu-sim.msa"
cuSpc = ept.SpectrumFile.open(cuFile)[0]
cuSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ws = wrap(cuSpc)
cuSpc = cropSpec(ws, end=maxCh)
cuSpc = setKeySimSpcProps(cuSpc, e0, dose)

unFile = unkDir + "95-nm-Ni-on-400-nm-Cu-15-kV.msa"
unSpc = ept.SpectrumFile.open(unFile)[0]
unSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ws = wrap(unSpc)
unSpc = cropSpec(ws, end=maxCh)
unSpc = setKeySimSpcProps(unSpc, e0, dose)




# display(oSpc)

cStd  = {"El":element("C"),  "Spc":cSpc}
oStd  = {"El":element("O"),  "Spc":oSpc}
niStd = {"El":element("Ni"), "Spc":niSpc}
cuStd = {"El":element("Cu"), "Spc":cuSpc}

stds = [cStd, oStd, niStd, cuStd]
a = compKRs(unSpc, stds, trs, det, e0)
print a



# clean up cruft
shutil.rmtree(rptPy)
print "Done!"
