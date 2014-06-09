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

defineStd(("Pd",),(1.000000,),"Pd",12.023000)
defineStd(("Zn",),(1.000000,),"Zn standard",7.100000)
# SRM 484. Data from Carpenter, Microanalysis Tools AMAS 2009 p. 32
defineStd(("Cu","Au",),(0.198300,0.801500,),"SRM-484",15.680800)
defineStd(("Cu",),(1.000000,),"Cu standard",8.960000)
defineStd(("Ni",),(1.000000,),"Ni",8.908000)
defineStd(("Fe","Ni",),(0.500000,0.500000,),"FeNi",8.960000)
defineStd(("Fe",),(1.000000,),"Fe standard",7.880000)
defineStd(("Mn",),(1.000000,),"Mn standard",7.410000)
# NaCl data from Wikipedia
defineStd(("Na","Cl",),(0.393372,0.606628,),"NaCl",2.160000)
# K496 data from Fournelle and SP260-112.pdf p.18
defineStd(("O","Mg","Al","P",),(0.5390,0.0665,0.0647,0.3298,),"K496",3.018000)
defineStd(("O","Mg","Si","Ca","Fe",),(0.423667,0.088465,0.253817,0.110563,0.112087,),"K411",5.000000)
defineStd(("O","Mg","Al","Si","Ca","Fe",),(0.427580,0.116567,0.049062,0.211982,0.108990,0.077420,),"K412")
defineStd(("O","Al",),(0.470749,0.529251,),"Al2O3",3.950000)
# Type 316 SS
# Data from http://www.nist.gov/srm/upload/SP260-73.PDF
# density from http://www.ask.com/answers/337173021/what-is-the-density-of-316-stainless-steel
defineStd(("C","P","S","Cr","Mn","Fe","Ni","Cu","Mo",),(0.000300,0.000100,0.000060,0.254300,0.001400,0.534140,0.209100,0.000400,0.000200,),"SS-316",7.990000)

# clean up cruft
shutil.rmtree(pyReptDir)
print "Done!"
