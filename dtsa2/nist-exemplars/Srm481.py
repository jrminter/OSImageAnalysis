# A script for simulating NIST SRM-481 - the Au/Ag series
# 22-Feb-2011 Nicholas W. M. Ritchie

import dtsa2.mcSimulate3 as mc3

det = d2  # Replace with yours (use listDetectors())
nE = 10
e0 = 20.0

rhoAu = 19.3
rhoAg = 10.49

SRM481A = material("Au",rhoAu)
SRM481B = epq.Material(epq.Composition(map(element,["Au","Ag"],),[0.800,0.199],"Au80Ag20"),epq.ToSI.gPerCC(0.8*rhoAu+0.2*rhoAg))
SRM481C = epq.Material(epq.Composition(map(element,["Au","Ag"],),[0.600,0.399],"Au60Ag40"),epq.ToSI.gPerCC(0.6*rhoAu+0.4*rhoAg))
SRM481D = epq.Material(epq.Composition(map(element,["Au","Ag"],),[0.400,0.599],"Au40Ag60"),epq.ToSI.gPerCC(0.4*rhoAu+0.6*rhoAg))
SRM481E = epq.Material(epq.Composition(map(element,["Au","Ag"],),[0.224,0.775],"Au20Ag80"),epq.ToSI.gPerCC(0.2*rhoAu+0.8*rhoAg))
SRM481F = material("Ag",rhoAg)

SRM481 = ( SRM481A, SRM481B, SRM481C, SRM481D, SRM481E, SRM481F, )

range = electronRange(SRM481A,e0,density=None)

xtraP = {}
xtraP.update(mc3.configureOutput(DefaultOutput))
xtraP.update(mc3.configurePhiRhoZ(1.5*range))
xtraP.update(mc3.configureEmissionImages(mc3.suggestTransitions(SRM481C,e0), 1.5*range, size = 512))
xtraP.update(mc3.configureTrajectoryImage(1.5*range, size = 512))

specs = {}
for mat in SRM481:
   specs[mat] = mc3.simulate(mat, det,e0=e0, nTraj=nE, dose=500.0, sf=True, bf=True,xtraParams=xtraP)
   specs[mat].save("%s/%s.msa" % ( DefaultOutput, specs[mat] ))
   specs[mat].display()
   

unks = ( specs[SRM481B], specs[SRM481C], specs[SRM481D], specs[SRM481E] )
stds = { "Au" : specs[SRM481A], "Ag" : specs[SRM481F] }

res = {}
for unk in unks:
   res[unk]=quantify(unk, stds, preferred = ( "Au L3-M5", "Ag L3-M5" ))
   
   
tabulate(unks)

# Finally output analytical model phi(rho z) curves for comparison
for mat in SRM481:
   phirhoz(mat,det,20.0)