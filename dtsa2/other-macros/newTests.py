import os
import dtsa2.mcNiCu as mcNiCu
edsDir = os.environ['EDS_ROOT']
relStd = "/CuNiSpc/dtsa-sim/corBulk"
stdBas = edsDir + relStd
# print(stdBas)
det = findDetector("FEI FIB620 EDAX-RTEM")
spc = mcNiCu.simNiCuPetSpc(200, 400, 15, det, wkDst=17, lt=100, pc=1, nTraj=1000)
display(spc)
kr = mcNiCu.anaMcNiCuKa(spc, det, stdBas, maxCh=1200)
print(kr)


import dtsa2.mcNiCu as mcNiCu
expl = [0.75273, 0.19565]
modl = [0.70000, 0.18900]
rd = mcNiCu.compKrRmsDev(expl, modl)
print(rd)

import dtsa2.jmGen as jmg
det =  findDetector("FEI CM20UT EDAX-RTEM")
spc = jmg.spcTopHatFilter(s1, det, 200, fw=150, norm=False)
display(spc)

import dtsa2.jmGen as jmg
en = jmg.getKalphaEnergy("Al")
print(en)
pInt = jmg.compPeakIntegral(s1, en, 150, digits=1)
print(pInt)


