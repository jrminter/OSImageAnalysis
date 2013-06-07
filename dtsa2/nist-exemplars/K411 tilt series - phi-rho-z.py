# A script for computing emitted intensities from particles as functions
# of the beam energy and particle size.

# Define the materials
k411 = epq.Material(epq.Composition([epq.Element.Ca,epq.Element.Fe,epq.Element.O,
                                     epq.Element.Mg, epq.Element.Si],
                                    [0.112, 0.112, 0.429, 0.092, 0.256] ),
                                    epq.ToSI.gPerCC(2.946))
k411.setName("SRM-2066")

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

for p in range(0,100,10):
   frac=p/100.0
   if terminated:
      break
   normal = [-frac,0.0,-jl.Math.sqrt(1.0-frac*frac)]
   print "%s" % normal
   if terminated:
      break
   det.reset()
   monte = nm.MonteCarloSS()
   gun=nm.GaussianBeam(1.0e-9)
   monte.setElectronGun(gun)
   monte.setBeamEnergy(epq.ToSI.keV(e0))
   # Create a plane of k411
   delta = [0.0,0.0,r*(1.0-jl.Math.sqrt(1.0-frac*frac))]
   monte.addSubRegion(monte.getChamber(),k411,nm.MultiPlaneShape.createSubstrate(normal,epu.Math2.plus(origin,delta)))
   # Add event listeners to model characteristic radiation
   xrel=nm.XRayEventListener2(monte,det)
   monte.addActionListener(xrel)
   prz=nm.PhiRhoZ(xrel, origin[2]+0.0, origin[2]+3.0*r, 100)
   xrel.addActionListener(prz)
   # Run the MC
   monte.runMultipleTrajectories(nTraj)
   # write the phi(rho z) curves
   pw = jio.PrintWriter("%s/phi-rho-z th=%g deg - %d.csv" % (DefaultOutput, jl.Math.asin(frac)*180.0/jl.Math.PI,p))
   prz.write(pw)
   pw.close()