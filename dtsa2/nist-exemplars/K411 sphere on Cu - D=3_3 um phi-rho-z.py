# A script for computing emitted intensities from particles as functions
# of the beam energy and particle size.

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

# Bookkeeping
r = 0.5*partDiameter # radius
# Other initialization
nTraj = 100000 # electrons

for p in range(0,111,10):
   frac = p/100.0
   if terminated:
      break
	# Iterate over a range of radii (in meters)
   det.reset()
   monte = nm.MonteCarloSS()
   gun=nm.GaussianBeam(1.0e-9)
   gun.setCenter([-frac*r,0.0,-0.01])
   monte.setElectronGun(gun)
   monte.setBeamEnergy(epq.ToSI.keV(e0))
   # Create a sphere of k411
   center = epu.Math2.plus(origin,[0.0,0.0,r])
   monte.addSubRegion(monte.getChamber(),k411,nm.Sphere(center,r))
   # Place it on a substrate
   monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], epu.Math2.plus(origin,[0.0,0.0,partDiameter])) )
   # Add event listeners to model characteristic radiation
   xrel=nm.XRayEventListener2(monte,det)
   monte.addActionListener(xrel)
   prz=nm.PhiRhoZ(xrel, origin[2]+0.0, origin[2]+3.0*r, 100)
   xrel.addActionListener(prz)
   # Run the MC
   monte.runMultipleTrajectories(nTraj)
   # Write the phi(rho z) curves
   pw = jio.PrintWriter("%s/phi-rho-z r=%d pct.csv" % (DefaultOutput, p))
   prz.write(pw)
   pw.close()