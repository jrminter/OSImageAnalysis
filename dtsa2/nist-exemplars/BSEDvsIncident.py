# File:   BSEDvsIncident.py
# A script for modeling the backscatter coefficient as a function of
# beam energy and incidence angle for various different pure elements.
# Author:  Nicholas W. M. Ritchie
# Date:    27-Feb-2009

import math

nTraj = 10000  # 10k gives ~1% precision

print "Material    \tE_0\tIncident\tBack\tForward\tAll"
for elm in [epq.Element.Al, epq.Element.Ti, epq.Element.Cu, epq.Element.Ag, epq.Element.Au]:
   for e0 in [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 50.0]:
      mat = epq.MaterialFactory.createPureElement(elm)
      for gamma in [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]:
         monte = nm.MonteCarloSS()
         monte.setBeamEnergy(epq.ToSI.keV(e0))
         # Create a sphere of Au with a sphere of K412 inside
         normal = [-sin(gamma/57.2958),0.0,-cos(gamma/57.2958)]
         # Place it on a carbon substrate
         monte.addSubRegion(monte.getChamber(), mat, nm.MultiPlaneShape.createSubstrate(normal, [0.0,0.0,0.0]))
         bsed=nm.BackscatterStats(monte)
         monte.addActionListener(bsed)
         monte.runMultipleTrajectories(nTraj)
         fos=jio.FileOutputStream("%s/%s at %g keV and %g deg.csv" % (DefaultOutput, mat, e0, gamma))
         bsed.dump(fos)
         print "%s\t%g\t%g\t%g\t%g\t%g"  % (mat, e0, gamma, bsed.backscatterFraction(), bsed.forwardscatterFraction(), bsed.scatterFraction())