import dtsa2.jmGen as jmg
spc = wrap(s1)
cr = jmg.cropSpec(spc, end=512)


import dtsa2.jmGen as jmg
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



cuFil = "C:/data/eds/CuNiSpc/dtsa-sim/corBulk/15kV/CuSim.msa"
niFil = "C:/data/eds/CuNiSpc/dtsa-sim/corBulk/15kV/Ni-Sim.msa"
unFil = "C:/data/eds/CuNiSpc/dtsa-sim/StrataGemNiCu/103-nm-Ni-on-198-nm-Cu-15-kV.msa"

spc = wrap(ept.SpectrumFile.open(niFil)[0])
spc = jmg.cropSpec(spc, end=maxCh)
niSpc = jmg.updateCommonSpecProps(spc, det, liveTime=liveTim, probeCur=probeCur, e0=e0, wrkDist=wrkDist)



import dtsa2.jmGen as jmg
ni  = material("Ni", density=8.90)
det=findDetector("FEI FIB620 EDAX-RTEM")
niSpc = jmg.simBulkSpcUnCor("Ni-sim", ni, det, e0=15, nTraj=100, lt=60, pc=1)
display(niSpc)







