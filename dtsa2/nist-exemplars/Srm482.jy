# A script for simulating NIST SRM-482 - the Au/Cu series
# 22-Feb-2011 Nicholas W. M. Ritchie

import dtsa2.mcSimulate3 as mc3

det = d2  # Replace with yours (use listDetectors())
nE = 10000
e0 = 20.0

rhoAu = 19.3
rhoCu = 8.95

SRM482A = material("Au",rhoAu)
SRM482B = epq.Material(epq.Composition(map(element,["Au","Cu"],),[0.801,0.198],"Au80Cu20"),epq.ToSI.gPerCC(0.8*rhoAu+0.2*rhoCu))
SRM482C = epq.Material(epq.Composition(map(element,["Au","Cu"],),[0.603,0.396],"Au60Cu40"),epq.ToSI.gPerCC(0.6*rhoAu+0.4*rhoCu))
SRM482D = epq.Material(epq.Composition(map(element,["Au","Cu"],),[0.401,0.599],"Au40Cu60"),epq.ToSI.gPerCC(0.4*rhoAu+0.6*rhoCu))
SRM482E = epq.Material(epq.Composition(map(element,["Au","Cu"],),[0.201,0.798],"Au20Cu80"),epq.ToSI.gPerCC(0.2*rhoAu+0.8*rhoCu))
SRM482F = material("Cu",rhoCu)

SRM482 = ( SRM482A, SRM482B, SRM482C, SRM482D, SRM482E, SRM482F, )

range = electronRange(SRM482A,e0,density=None)

xtraP = {}
xtraP.update(mc3.configureOutput(DefaultOutput))
xtraP.update(mc3.configurePhiRhoZ(1.5*range))
xtraP.update(mc3.configureEmissionImages(mc3.suggestTransitions(SRM482C,e0), 1.5*range, size = 512))
xtraP.update(mc3.configureTrajectoryImage(1.5*range, size = 512))

specs = {}
for mat in SRM482:
   if terminated:
      break
   specs[mat] = mc3.simulate(mat, det,e0=e0, nTraj=nE, dose=500.0, sf=True, bf=True,xtraParams=xtraP)
   specs[mat].save("%s/%s.msa" % ( DefaultOutput, specs[mat] ))
   specs[mat].display()
   

unks = ( specs[SRM482B], specs[SRM482C], specs[SRM482D], specs[SRM482E] )
stds = { "Au" : specs[SRM482A], "Cu" : specs[SRM482F] }

res = {}
for unk in unks:
   res[unk]=quantify(unk, stds, preferred = ( "Au L3-M5", "Cu K-L3" ))
   
   
tabulate(unks)

# Finally output analytical model phi(rho z) curves for comparison
for mat in SRM482:
   phirhoz(mat,det,20.0)