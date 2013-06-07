# A script for computing emitted intensities from particles as functions
# of the beam energy and particle size.

from jarray import zeros

# Define the materials
k411 = epq.Material(epq.Composition([epq.Element.Ca,epq.Element.Fe,epq.Element.O,
                                     epq.Element.Mg, epq.Element.Si],
                                    [0.112, 0.112, 0.429, 0.092, 0.256] ),
                                    epq.ToSI.gPerCC(2.946))
k411.setName("SRM-2066")
c = epq.MaterialFactory.createPureElement(epq.Element.Cu)

# Place the sample at the optimal location for the detector
det = findDetector("Bruker 10")
origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())

e0=25.0    # beam energy
# Particle size
partDiameter = 3.3e-6
# Map dimensions
xSize = 160
ySize = 120
# Location of the particle
xCenter = 76
yCenter = 59

# Bookkeeping
r = 0.5*partDiameter # radius
pixSize = (2*r)/108.3
depth = 2048
test=false
# Other initialization
dose = 150.0e-9 # A*sec
nTraj = 100000 # electrons

for p in range(0,111,10):
   if terminated:
      break
   rp = (p*r)/100.0
   x = xCenter-rp/pixSize
   y=yCenter
   print "%d, %d" % (x,y)
# Iterate over a range of radii (in meters)
   if terminated:
      break
   name = "E0 = %g keV R = %g um %s" % (e0, r/1.0e-6, k411)
   det.reset()
   monte = nm.MonteCarloSS()
   gun=nm.GaussianBeam(1.0e-9)
   gun.setCenter([(x-75)*pixSize,(59-y)*pixSize,-0.01])
   monte.setElectronGun(gun)
   monte.setBeamEnergy(epq.ToSI.keV(e0))
   # Create a sphere of k411
   center = epu.Math2.plus(origin,[0.0,0.0,r])
   monte.addSubRegion(monte.getChamber(),k411,nm.Sphere(center,r))
   # Place it on a carbon substrate
   monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], epu.Math2.plus(origin,[0.0,0.0,2*r])) )
   # Add event listeners to look for forward and back scattered electrons
   below=nm.AnnularDetector(10.0*r, 100, epu.Math2.plus(origin,[0.0,0.0,2*r]), [0.0, 0.0, -1.0]);
   belowAll=nm.AnnularDetector(1.0, 1, epu.Math2.plus(origin,[0.0,0.0,2*r]), [0.0, 0.0, -1.0]);
   above=nm.AnnularDetector(1.0, 1, origin, [0.0, 0.0, 1.0])
   monte.addActionListener(below)
   monte.addActionListener(belowAll)
   monte.addActionListener(above)
   # Run the MC
   monte.runMultipleTrajectories(nTraj)
   pw=jio.PrintWriter("%s/scatter %d.csv" % (DefaultOutput, p))
   pw.println("Above")
   above.dump(pw)
   pw.println("Below (summary)")
   belowAll.dump(pw)
   pw.println("Below")
   below.dump(pw)
   pw.close()
