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
# Transitions to watch...
xrts = [
   epq.XRayTransition(epq.Element.Ca,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Fe,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Fe,epq.XRayTransition.LA1),
   epq.XRayTransition(epq.Element.O,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Mg,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Si,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Cu,epq.XRayTransition.KA1),
   epq.XRayTransition(epq.Element.Cu,epq.XRayTransition.LA1) ]


e0=25.0    # beam energy
# Particle size
partDiameter = 3.3e-6
# Map dimensions
xSize = 160
ySize = 120
# Location of the particle
xCenter = 76
yCenter = 59

# Split the task up to run on multiple CPUs
xStride = 4
yStride = 2

# Bookkeeping
r = 0.5*partDiameter # radius
pixSize = (2*r)/108.3
depth = 2048
test=false
# Other initialization
dose = 150.0e-9 # A*sec
nTraj = 1000 # electrons

path="%s/%s_[%d,%d].%s" % ( DefaultOutput,k411,offset % xStride, offset / xStride,"%s")
print path
res = ept.RippleFile(xSize,ySize,depth,ept.RippleFile.SIGNED,4,ept.RippleFile.DONT_CARE_ENDIAN,path % "rpl", path % "raw")
path="%s/%s I_[%d,%d].%s" % ( DefaultOutput,k411,offset % xStride, offset / xStride,"%s")
print path
resXrts = ept.RippleFile(xSize,ySize,len(xrts),ept.RippleFile.FLOAT,4,ept.RippleFile.DONT_CARE_ENDIAN,path % "rpl", path % "raw")

for x in range(offset % xStride, xSize, xStride):
   if terminated:
      break
   for y in range(offset / xStride, ySize, yStride):
      print "%d, %d" % (x,y)
   # Iterate over a range of radii (in meters)
      if terminated:
         break
      if not test:
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
         scale = dose / (nTraj * epq.PhysicalConstants.ElectronCharge)
         spec=det.getSpectrum(scale)
         if false:
            props=spec.getProperties()
            props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,name)
            props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose*1.0e9)
            props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
            props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
         d=epq.SpectrumUtils.toIntArray(spec)
      else:
         d=zeros(depth,'i')
         for i in range(0,depth):
            d[i]=x+i % (y+1)
      res.seek(y, x)
      res.write(d[0:depth])
      if not test:
         # Write the spectrum to disk and display
         fos = jio.FileOutputStream("%s/%s[%d,%d].msa" % (DefaultOutput, k411, x, y))
         # noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
         ept.WriteSpectrumAsEMSA1_0.write(spec,fos,0)
         fos.close()
         xa.setScale(scale)
         tmp=[]
         for xrt in xrts:
            tmp=tmp+[xa.getEmitted(xrt)]
         resXrts.seek(y, x)
         resXrts.write(tmp)

res.close()
resXrts.close()