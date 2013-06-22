# -*- coding: utf-8 -*-

def defineStd(elms,qty,name,density=None):
	c=epq.Composition(map(element,elms),qty,name)
	if density:
		c=epq.Material(c,epq.ToSI.gPerCC(density))
	Database.addStandard(c)

defineStd(("Zn",),(1.000000,),"Zn standard",7.100000)
defineStd(("Cu",),(1.000000,),"Cu",8.290000)
defineStd(("Cu",),(1.000000,),"Cu standard",8.960000)
defineStd(("Fe",),(1.000000,),"Fe standard",7.880000)
defineStd(("Mn",),(1.000000,),"Mn standard",7.410000)
defineStd(("O","Mg","Si","Ca","Fe",),(0.423667,0.088465,0.253817,0.110563,0.112087,),"K411",5.000000)
defineStd(("O","Mg","Al","Si","Ca","Fe",),(0.427580,0.116567,0.049062,0.211982,0.108990,0.077420,),"K412")
# SRM 484. Data from Carpenter, Microanalysis Tools AMAS 2009
# p. 32
defineStd(("Cu","Au",),(0.1983,0.8015,),"SRM-484", 15.6808)
# Type 316 SS
# Data from http://www.nist.gov/srm/upload/SP260-73.PDF
# density from http://www.ask.com/answers/337173021/what-is-the-density-of-316-stainless-steel
defineStd(("Fe","Cr","Ni","Mn","Cu","C","Mo","P","S",),(0.53414,0.2543,0.2091,0.0014,0.0004,0.0003,0.0002,0.0001,0.00006,),"SS-316", 7.99)



