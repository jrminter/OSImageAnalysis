# A script for simulating an x-ray hyperspectral map of SRM-2066 microsphere glass particles.
# The script models a microsphere of K411 glass and performs a Monte Carlo simulation
# to estimate the emitted intensity as a function of position.  The resulting spectra
# are output to a LISTPIX-style Ripple/Raw file as spectra and as x-ray intensities.
# Author:  Nicholas Ritchie
# Updated: 5-Jan-2008

from jarray import zeros

det = findDetector("Bruker 10")
nTraj = 1000 # electrons
dose = 150 # nA*sec
substrate = 0

# Define the materials
k411 = epq.Material(epq.Composition([epq.Element.Ca,epq.Element.Fe,epq.Element.O,
                                     epq.Element.Mg, epq.Element.Si],
                                    [0.112, 0.112, 0.429, 0.092, 0.256] ),
                                    epq.ToSI.gPerCC(5.0))
k411.setName("SRM-2066")
c = epq.MaterialFactory.createPureElement(epq.Element.C)

xrts = [
   epq.XRayTransition(epq.Element.Ca,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Fe,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Fe,epq.XRayTransition.LA1),
   epq.XRayTransition(epq.Element.O,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Mg,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Si,epq.XRayTransition.KA1) ]

# Place the sample at the optimal location for the detector
origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())

e0=25.0    # beam energy
r = 7.2e-6 # radius
size = 64
depth = 2048
test=false

quadrant = 0

path="%s/SRM-2006_%d.%s" % ( DefaultOutput,quadrant,"%s")
res = ept.RippleFile(size,size,depth,ept.RippleFile.SIGNED,4,ept.RippleFile.DONT_CARE_ENDIAN,path % "rpl", path % "raw")
path="%s/SRM-2006 I_%d.%s" % ( DefaultOutput,quadrant,"%s")
resXrts = ept.RippleFile(size,size,len(xrts),ept.RippleFile.FLOAT,4,ept.RippleFile.DONT_CARE_ENDIAN,path % "rpl", path % "raw")

xmin=(quadrant%2)*size/2
ymin=((quadrant/2)%2)*size/2

for x in range(0,size):
   if terminated:
      break
   print "%d" % (x)
   for y in range(ymin,ymin+size/2):
   # Iterate over a range of radii (in meters)
      if terminated:
         break
      name = "E0 = %g keV R = %g um %s" % (e0, r/1.0e-6, k411)
      det.reset()
      monte = nm.MonteCarloSS()
      gun=nm.GaussianBeam(1.0e-9)
      gun.setCenter([2.0*r*((1.0*x)/size - 0.5),2*r*((1.0*y)/size - 0.5),-0.01])
      monte.setElectronGun(gun)
      monte.setBeamEnergy(epq.ToSI.keV(e0))
      # Create a sphere of k411
      center = epu.Math2.plus(origin,[0.0,0.0,r])
      monte.addSubRegion(monte.getChamber(),k411,nm.Sphere(center,r))
      # Place it on a carbon substrate
      monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], epu.Math2.plus(origin,[0.0,0.0,2*r])) )
      # Add event listeners to model characteristic radiation
      xrel=nm.XRayEventListener2(monte,det)
      monte.addActionListener(xrel)
      xa=nm.XRayAccumulator(xrts)
      xrel.addActionListener(xa)
      brem=nm.BremsstrahlungEventListener(monte,det)
      monte.addActionListener(brem)
      # Create a simulator and initialize it
      # Run the MC
      monte.runMultipleTrajectories(nTraj)
      # Get the spectrum and assign properties
      scale = (dose*1.0e-9) / (nTraj * epq.PhysicalConstants.ElectronCharge)
      spec=det.getSpectrum(scale)
      props=spec.getProperties()
      props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,name)
      props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
      props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
      props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
      d=epq.SpectrumUtils.toIntArray(spec)
      res.seek(x,y)
      res.write(d[0:depth])
      # Write the spectrum to disk and display
      fos = jio.FileOutputStream("%s/%s[%d,%d].msa" % (DefaultOutput, k411, x, y))
      # noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
      ept.WriteSpectrumAsEMSA1_0.write(spec,fos,0)
      fos.close()
      xa.setScale(scale)
      tmp=[]
      for xrt in xrts:
         tmp=tmp+[xa.getEmitted(xrt)]
      resXrts.seek(x,y)
      resXrts.write(tmp)

res.close()
resXrts.close()