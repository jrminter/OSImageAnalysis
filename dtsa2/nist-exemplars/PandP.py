# A script which iterates throught the PAP database of measured k-ratios
# and performs a Monte Carlo simulation to compare measured and simulated
# k-ratios.
# Author:  Nicholas W. M. Ritchie
# Date:    14-Aug-2009

nTraj = 20000

def calculateI(mat, xrt, e0, toa):
   det = epq.Detector.EDSDetector.createSiLiDetector(4096,5,130.0)
   det.getDetectorProperties().getProperties().setDetectorPosition(toa,0.0,20.0e-3,12.0e-3)
   origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())
   detPos = epq.SpectrumUtils.getDetectorPosition(det.getProperties())
   # Create a simulator and initialize it
   monte = nm.MonteCarloSS()
   monte.setBeamEnergy(e0)
   
   monte.addSubRegion(monte.getChamber(),mat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], origin) )
   # Add event listeners to model characteristic radiation
   
   xrel=nm.XRayEventListener2(monte,det)
   monte.addActionListener(xrel)
   acc = nm.XRayAccumulator([xrt])
   xrel.addActionListener(acc)
   det.reset()
   monte.runMultipleTrajectories(nTraj)
   return acc.getEmitted(xrt)

ppd = epq.PandPDatabase()
res=textFile(DefaultOutput+"/result.csv")
for i in range(0,ppd.getSize()):
   if terminated:
      break
   mat = ppd.createMaterial(i)
   std = ppd.createStandard(i)
   elmA = ppd.elementA(i)
   elmB = ppd.elementB(i)
   th = ppd.takeOffAngle(i)
   e0 = ppd.beamEnergy(i)
   xrt = ppd.transition(i)
   kEx = ppd.kRatio(i)
   kSim = calculateI(mat,xrt,e0,th)/calculateI(std,xrt,e0,th)
   res.println("%s\t%s\t%s\t%s\t%g\t%g\t%s\t%g\t%g" % (mat, std, elmA, elmB, jl.Math.toDegrees(th), epq.FromSI.keV(e0), xrt, kEx, kSim))
res.close()   