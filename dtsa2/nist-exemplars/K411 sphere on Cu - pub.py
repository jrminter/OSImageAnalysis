# K411 sphere on Cu.py - DTSA-II Python script
# A script for computing an x-ray spectrum image of a K411 glass
# sphere on a copper substrate.
# Author:            Nicholas W. M. Ritchie  
# Last modified:     3-Feb-2009
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

e0=25.0                 # beam energy (keV)
partDiameter = 3.3e-6   # particle size (meters)
size =  [ 160, 120 ]    # map dimensions
center = [ 76, 59 ]     # particle center (pixels)
stride = [ 4, 2 ]       # split the task up to run on multiple CPUs

# Bookkeeping
r = 0.5*partDiameter    # particle radius
pixSize = (2*r)/108.3   # edge length of a single pixel (meters)
depth = 2048            # pixel depth in spectrum image
dose = 150.0e-9         # A*sec
nTraj = 1000            # electrons
# Output files
path="%s/%s_[%d,%d].%s" % ( DefaultOutput,k411,offset % stride[0], offset / stride[0],"%s")
print path
res = ept.RippleFile(size[0],size[1],depth,ept.RippleFile.SIGNED,4,ept.RippleFile.DONT_CARE_ENDIAN,
            path % "rpl", path % "raw")
# Iterate over each pixel in the spectrum image
for x in range(offset % stride[0], size[0], stride[0]):
   if terminated:
      break
   for y in range(offset / stride[0], size[1], stride[1]):
      print "%d, %d" % (x,y)
      if terminated:
         break
      det.reset()       # clear the detector accumulator
      monte = nm.MonteCarloSS()
      gun=nm.GaussianBeam(1.0e-9)
      gun.setCenter([(x-center[0])*pixSize,(center[1]-y)*pixSize,-0.01])
      monte.setElectronGun(gun)
      monte.setBeamEnergy(epq.ToSI.keV(e0))
      # Create a sphere of k411
      center = epu.Math2.plus(origin,[0.0,0.0,r])
      monte.addSubRegion(monte.getChamber(),k411,nm.Sphere(center,r))
      # Place it on a carbon substrate
      monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], 
         epu.Math2.plus(origin,[0.0,0.0,2*r])) )
      # Add event listeners to model characteristic and Bremsstrahlung radiation
      xrel=nm.XRayEventListener2(monte,det)
      monte.addActionListener(xrel)
      brem=nm.BremsstrahlungEventListener(monte,det)
      monte.addActionListener(brem)
      # Run the MC
      monte.runMultipleTrajectories(nTraj)
      # Get the spectrum and assign properties
      scale = dose / (nTraj * epq.PhysicalConstants.ElectronCharge)
      spec=det.getSpectrum(scale)
      res.seek(y, x)
      res.write(epq.SpectrumUtils.toIntArray(spec)[0:depth])
      # Write the spectrum to disk and display
      fos = jio.FileOutputStream("%s/%s[%d,%d].msa" % (DefaultOutput, k411, x, y))
      ept.WriteSpectrumAsEMSA1_0.write(spec,fos,0)
      fos.close()
res.close()             # close the ripple file
