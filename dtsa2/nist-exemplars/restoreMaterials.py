# -*- coding: utf-8 -*-

def defineStd(elms,qty,name,density=None):
    c=epq.Composition(map(element,elms),qty,name)
    if density:
        c=epq.Material(c,epq.ToSI.gPerCC(density))
    Database.addStandard(c)

defineStd(("Ta",),(1.000000,),"Ta",16.400000)
defineStd(("Pd","Au",),(0.400000,0.600000,),"Au-Pd",16.340000)
defineStd(("Pd",),(1.000000,),"Pd",12.023000)
defineStd(("Zn",),(1.000000,),"Zn standard",7.100000)
defineStd(("Cu","Au",),(0.198300,0.801500,),"SRM-484",15.680800)
defineStd(("Cu",),(1.000000,),"Cu",8.960000)
defineStd(("Ni",),(1.000000,),"Ni",8.908000)
defineStd(("Fe","Ni",),(0.500000,0.500000,),"FeNi",8.960000)
defineStd(("Fe",),(1.000000,),"Fe standard",7.880000)
defineStd(("Mn",),(1.000000,),"Mn standard",7.410000)
defineStd(("Na","Cl",),(0.393372,0.606628,),"NaCl",2.160000)
defineStd(("O","Mg","Si","Ca","Fe",),(0.423667,0.088465,0.253817,0.110563,0.112087,),"K411",2.946000)
defineStd(("O","Mg","Al","Si","Ca","Fe",),(0.427580,0.116567,0.049062,0.211982,0.108990,0.077420,),"K412")
defineStd(("O","Al",),(0.470749,0.529251,),"Al2O3",3.950000)
defineStd(("O","Mg","Al","P",),(0.539000,0.066500,0.064700,0.329800,),"K496",3.018000)
defineStd(("C","P","S","Cr","Mn","Fe","Ni","Cu","Mo",),(0.000300,0.000100,0.000060,0.254300,0.001400,0.534140,0.209100,0.000400,0.000200,),"SS-316",7.990000)
defineStd(("B","Ti",),(0.311157,0.688843,),"TiB2",4.520000)
defineStd(("H","C","O",),(0.041960,0.625020,0.069042,),"PET",1.370000)