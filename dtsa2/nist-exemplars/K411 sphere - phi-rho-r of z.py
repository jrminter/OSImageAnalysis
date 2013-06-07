# A script for computing the radial distribution of emission as a function of depth

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

det.reset()
monte = nm.MonteCarloSS()
gun=nm.GaussianBeam(1.0e-9)
monte.setElectronGun(gun)
monte.setBeamEnergy(epq.ToSI.keV(e0))
center = epu.Math2.plus(origin,[0.0,0.0,r])
monte.addSubRegion(monte.getChamber(),k411,nm.Sphere(center,r))
# Place it on a carbon substrate
monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], epu.Math2.plus(origin,[0.0,0.0,2*r])) )
# Add event listeners to model characteristic radiation
xrel=nm.XRayEventListener2(monte,det)
monte.addActionListener(xrel)
prz=nm.PhiRhoRofZ(xrel, origin[2], origin[2]+6.0e-6, 10, 5.0e-6, 20 )
xrel.addActionListener(prz)
# Run the MC
monte.runMultipleTrajectories(nTraj)
# Get the spectrum and assign properties
pw = jio.PrintWriter("%s/phi-rho-r of z (2).csv" % (DefaultOutput))
prz.write(pw)
pw.close()