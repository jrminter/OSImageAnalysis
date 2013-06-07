# Replicating the calculation performed in the CITZAF manual using DTSA-II
#  The manual demonstrates correcting 6 measurements taken from Kakanue Horneblende
#  using Albite, Forsterite, Microline, Brookite, Cr2O3 and Garnet as standards.
# 29-Nov-2008 NWMR
albite = epq.Material(parseChemicalFormula("NaAlSi3O8"),epq.ToSI.gPerCC(2.62))
albite.setName("Albite")

ameliaAlbite = epq.Material(epq.Composition(
               elements(["Na","Al","Si","K","O"]),
               [0.0872, 0.1028, 0.3213, 0.0007, 0.4880]),
               epq.ToSI.gPerCC(2.62))
ameliaAlbite.setName("Amelia Albite")

boydForsterite = epq.Material(epq.Composition(
               elements(["Mg","Si","Mn","Fe","Ni","O"]),
               [0.3114,0.1910,0.0005,0.0562,0.0024,0.4394]),
               epq.ToSI.gPerCC(3.27))
boydForsterite.setName("Boyd Forsterite")

anorthite = epq.Material(parseChemicalFormula("CaAl2Si2O8"),epq.ToSI.gPerCC(2.73))
anorthite.setName("Anorthite")

asbMicrocline = epq.Material(epq.Composition(
               elements(["Na","Mg","Al","Si","K","Ca","Fe","Ba","O"]),
               [0.0013,0.0001,0.0972,0.2992,0.1354,0.0013,0.0002,0.0009,0.4562]),
               epq.ToSI.gPerCC(2.56))
asbMicrocline.setName("Asb. Microcline")

brookite = epq.Material(parseChemicalFormula("TiO2"),epq.ToSI.gPerCC(4.11))
brookite.setName("Brookite")

cr2o3 = epq.Material(parseChemicalFormula("Cr2O3"),epq.ToSI.gPerCC(5.21))
cr2o3.setName("Chromium(III) oxide")

nuevoGarnet = epq.Material(epq.Composition(
                elements(["Mg","Al","Si","Ca","Ti","Mn","Fe","O"]),
                [0.0018,0.1058,0.1691,0.0027,0.0002,0.1630,0.1691,0.3851]),
                epq.ToSI.gPerCC(4.25))
nuevoGarnet.setName("Nuevo Garnet")

stds = [ [ "Na", ameliaAlbite ],
  [ "Mg", boydForsterite ],
  [ "Al", anorthite ],
  [ "Si", ameliaAlbite ],
  [ "K", asbMicrocline ],
  [ "Ca", anorthite ],
  [ "Ti", brookite ],
  [ "Cr", cr2o3 ],
  [ "Mn", nuevoGarnet ],
  [ "Fe", boydForsterite ] ]
  
for std in stds:
   std[0] = epq.XRayTransitionSet(epq.XRayTransition(element(std[0]),epq.XRayTransition.KA1))
   std[1].forceNormalization()

unks = [ [ 0.187600, 0.225838, 0.345781, 0.567676, 0.131022, 0.510617, 0.044217, -0.000466, 0.003053, 1.498190 ],
  [ 0.190322, 0.224663, 0.344466, 0.570659, 0.133539, 0.514212, 0.044881, 0.000126, 0.004127, 1.507243 ],
  [ 0.189906, 0.223568, 0.344079, 0.570968, 0.133432, 0.513636, 0.044561, 0.000134, 0.003345, 1.486724 ],
  [ 0.192093,   0.223266,   0.343596, 0.570816, 0.132012, 0.512762, 0.044816, -0.000078, 0.004103, 1.493996 ],
  [ 0.189505,   0.223970,   0.343846, 0.570696, 0.129945, 0.511596, 0.045429, -0.000127, 0.002515, 1.455819 ],
  [ 0.184768,   0.223791,   0.342881, 0.571667, 0.130683, 0.515331, 0.045176, -0.000026, 0.004273, 1.502195 ] ]

sp = epq.SpectrumProperties()
sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy,15.0)
sp.setNumericProperty(epq.SpectrumProperties.TakeOffAngle,40.0)
sp.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
sp.setNumericProperty(epq.SpectrumProperties.LiveTime,60.0)

if true:
   qa = epq.CompositionFromKRatios()
   ebs = epq.CompositionFromKRatios.ElementByStoichiometry(epq.Element.O,-2.0,0)
   ebs.add(epq.Element.Na,1.0)
   ebs.add(epq.Element.Mg,2.0)
   ebs.add(epq.Element.Al,3.0)
   ebs.add(epq.Element.Si,4.0)
   ebs.add(epq.Element.K,1.0)
   ebs.add(epq.Element.Ca,2.0)
   ebs.add(epq.Element.Ti,4.0)
   ebs.add(epq.Element.Cr,3.0)
   ebs.add(epq.Element.Mn,2.0)
   ebs.add(epq.Element.Fe,2.0)
   qa.addUnmeasuredElementRule(ebs)

   st=epq.Strategy()
   ca=epq.CorrectionAlgorithm.Armstrong1982
   mac=epq.MassAbsorptionCoefficient.DTSA_CitZAF
   st.addAlgorithm(epq.CorrectionAlgorithm,ca)
   st.addAlgorithm(epq.MassAbsorptionCoefficient,mac)
   epq.AlgorithmUser.applyGlobalOverride(st)
   print "\nXRT by Z\tMAC"
   for alg in st.getAlgorithms():
      print "%s\t%s\n\t%s" % (alg.getAlgorithmClass(),alg.getName(),alg.getReference())
   print "\nStandards"
   for std in stds:
      qa.addStandard(std[0],std[1],sp)
      print "%s\t%s" % (std[0], std[1].descriptiveString(0))

   for stdA in stds:
      xrtA=stdA[0].iterator().next()
      for stdB in stds:
         elmB=stdB[0].iterator().next().getElement()
         print "%s by %s\t %g" % ( xrtA, elmB, mac.toCmSqrPerGram(mac.compute(elmB,xrtA)) )

   print "\nUnknowns"
   for unk in unks:
      krs=epq.KRatioSet()
      i=0
      for kr in unk:
         krs.addKRatio(stds[i][0],epu.UncertainValue(kr,0.00))
         i=i+1
      comp = qa.compute(krs,sp)
      print "%s\t%d" % (comp, krs.difference(qa.getBestKRatioSet())*1.0e6)
      print "XRT\tz(pure)\ta(pure)\tf(pure)\tz(rel)\ta(rel)\tf(rel)\tZ(pure)"
      for std in stds:
         xrt=std[0].iterator().next()
         if comp.containsElement(xrt.getElement()):
            cs=epq.Composition([xrt.getElement()],[1.0]) 
            pure=ca.relativeZAF(comp,xrt,sp,cs)           
            rel=ca.relativeZAF(comp,xrt,sp,std[1])           
            print "%s\t%g\t%g\t%g\t%g\t%g\t%g\t%g" % ( std[0], pure[0], pure[1], pure[2], rel[0], rel[1], rel[2], ca.relativeZ(comp,xrt,sp))            

if true:
   print "\nCitZAF results - CitZAF 3.06"
   print "Measurement Na   Mg   Al   Si    K    Ca   Ti   Cr   Mn   Fe   O     Total"
   print "          1 1.98 7.79 7.75 19.02 1.74 7.26 2.86 0.00 0.05 8.33 41.94 98.72"
   print "          2 2.01 7.76 7.71 19.10 1.77 7.31 2.91 0.01 0.07 8.38 42.07 99.10"
   print "          3 2.00 7.72 7.70 19.11 1.77 7.30 2.89 0.01 0.06 8.27 41.98 98.81"
   print "          4 2.02 7.71 7.69 19.10 1.75 7.29 2.90 0.00 0.07 8.31 41.99 98.83"
   print "          5 1.99 7.72 7.69 19.10 1.72 7.27 2.94 0.00 0.04 8.10 41.92 98.49"
   print "          6 1.95 7.73 7.68 19.13 1.73 7.32 2.93 0.00 0.07 8.35 42.03 98.92"

