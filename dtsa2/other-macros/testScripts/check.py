import dtsa2.jmGen as jmg
import os

edsDir = os.environ['EDS_ROOT']
relMsa = "/CuNiSpc/dtsa-sim/"
msaDir = edsDir + relMsa


jmg.clearAllSpectra()

det = findDetector("FEI FIB620 EDAX-RTEM")
liveTim  =   100 # sec
probeCur =     1 # nA
wrkDist  =    17 # mm
e0       =    15 # kV
maxCh    =  1200

# define the transitions I want to measure
trs = [epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.K_FAMILY),
epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.K_FAMILY)]



niFil = msaDir + "/corBulk/15kV/Ni-Sim.msa"
spc = wrap(ept.SpectrumFile.open(niFil)[0])
spc = jmg.cropSpec(spc, end=maxCh)
niSpc = jmg.updateCommonSpecProps(spc, det, liveTime=liveTim, probeCur=probeCur, e0=e0, wrkDist=wrkDist)

cuFil = msaDir + "/corBulk/15kV/Cu-Sim.msa"
spc = wrap(ept.SpectrumFile.open(cuFil)[0])
spc = jmg.cropSpec(spc, end=maxCh)
cuSpc = jmg.updateCommonSpecProps(spc, det, liveTime=liveTim, probeCur=probeCur, e0=e0, wrkDist=wrkDist)

unFil = msaDir + "/StrataGemNiCu/103-nm-Ni-on-198-nm-Cu-15-kV.msa"
spc = wrap(ept.SpectrumFile.open(unFil)[0])
spc = jmg.cropSpec(spc, end=maxCh)
unSpc = jmg.updateCommonSpecProps(spc, det, liveTime=liveTim, probeCur=probeCur, e0=e0, wrkDist=wrkDist)

niStd = {"El":element("Ni"), "Spc":niSpc}
cuStd = {"El":element("Cu"), "Spc":cuSpc}
stds  = [niStd, cuStd]

theKR = jmg.compKRs(unSpc, stds, trs, det, e0)

print(theKR)




