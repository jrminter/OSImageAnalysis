# -*- coding: utf-8 -*-
import os
import sys
import shutil
# Local system configuration options
gitHome=os.environ['GIT_HOME']
pyReptDir = gitHome + "/OSImageAnalysis/dtsa2/productionScripts/stds Results/"

def defineStd(elms,qty,name,density=None):
    c=epq.Composition(map(element,elms),qty,name)
    if density:
        c=epq.Material(c,epq.ToSI.gPerCC(density))
    Database.addStandard(c)


defineStd(("Ag",),(1.000000,),"Ag",10.490000)
defineStd(("Pd","Au",),(0.350774,0.649226,),"AuPd",11.500000)
defineStd(("Pd",),(1.000000,),"Pd",12.023000)
defineStd(("Zn",),(1.000000,),"Zn standard",7.100000)
# SRM 484. Data from Carpenter, Microanalysis Tools AMAS 2009 p. 32
defineStd(("Cu","Au",),(0.198300,0.801500,),"SRM-484",15.680800)
defineStd(("Cu",),(1.000000,),"Cu",8.096000)
defineStd(("Cu",),(1.000000,),"Cu standard",8.960000)
defineStd(("Ni",),(1.000000,),"Ni",8.908000)
defineStd(("Fe","Ni",),(0.500000,0.500000,),"FeNi",8.960000)
defineStd(("Fe",),(1.000000,),"Fe standard",7.880000)
defineStd(("Mn",),(1.000000,),"Mn standard",7.410000)
defineStd(("Cr","Fe","Ni",),(0.250000,0.550000,0.200000,),"SS309",7.890000)
defineStd(("Cl","Ca",),(0.638885,0.361115,),"CaCl2",2.150000)
defineStd(("Mg","Al",),(0.050000,0.950000,),"Henoc",2.652000)
# NaCl data from Wikipedia
defineStd(("Na","Cl",),(0.393372,0.606628,),"NaCl",2.160000)
defineStd(("Na","Cl",),(0.393372,0.606628,),"NaCl",2.160000)
defineStd(("O","Zn",),(0.196530,0.803470,),"ZnO",5.610000)
defineStd(("O","Al","Zn",),(0.198410,0.006690,0.794900,),"AZO-2",5.610000)
defineStd(("O","Al","Zn",),(0.201280,0.016970,0.781740,),"AZO-5",5.610000)
defineStd(("O","Fe",),(0.276410,0.723590,),"Fe3O4",5.170000)
defineStd(("O","Fe",),(0.300570,0.699430,),"Fe2O3",5.242000)
defineStd(("O","Ti",),(0.400660,0.599340,),"TiO2",4.230000)
defineStd(("O","Mg","Si","Ca","Fe",),(0.423667,0.088465,0.253817,0.110563,0.112087,),"K411",2.600000)
defineStd(("O","Mg","Al","Si","Ca","Fe",),(0.427580,0.116567,0.049062,0.211982,0.108990,0.077420,),"K412",2.600000)
defineStd(("O","V",),(0.439834,0.560166,),"V2O5",3.360000)
defineStd(("O","Al",),(0.470749,0.529251,),"Al2O3",3.950000)
defineStd(("O","Si",),(0.532565,0.467435,),"SiO2",2.650000)
# K496 data from Fournelle and SP260-112.pdf p.18
defineStd(("O","Mg","Al","P",),(0.539000,0.066500,0.064700,0.329800,),"K496",3.018000)
# Type 316 SS
# Data from http://www.nist.gov/srm/upload/SP260-73.PDF
# density from http://www.ask.com/answers/337173021/what-is-the-density-of-316-stainless-steel
defineStd(("C","P","S","Cr","Mn","Fe","Ni","Cu","Mo",),(0.000300,0.000100,0.000060,0.254300,0.001400,0.534140,0.209100,0.000400,0.000200,),"SS-316",7.990000)
defineStd(("C","O","Ca",),(0.120003,0.479565,0.400432,),"CaCO3",2.710000)
defineStd(("C","F",),(0.240182,0.759818,),"C2F4",3.340000)
defineStd(("C",),(1.000000,),"C",2.100000)
defineStd(("B","Ti",),(0.311157,0.688843,),"TiB2",4.520000)
defineStd(("H","C","N","O",),(0.026360,0.691130,0.073270,0.209240,),"Kapton",1.420000)
defineStd(("H","O","Ca",),(0.027208,0.431875,0.540917,),"Ca(OH)2",2.221000)
defineStd(("H","C","O",),(0.041960,0.625020,0.069042,),"PET",1.370000)
defineStd(("H","C","O","S",),(0.042536,0.506867,0.225065,0.225531,),"EDOT",1.000000)
defineStd(("H","C","N",),(0.056986,0.679049,0.263965,),"PAN",1.184000)
defineStd(("H","C","O",),(0.080542,0.599840,0.319618,),"PMMA",1.180000)

# clean up cruft
shutil.rmtree(pyReptDir)
print "Done!"
