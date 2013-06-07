# A script for simulating blocks of various sizes and orientations and
# comparing the quantification of the resulting spectra using Armstrong's
# CITZAF code.
# Author:  Nicholas Ritchie
# Updated: 28-Apr-2008

import java.util as ju

det = findDetector("Bruker 5")
nTraj = 1000 # electrons
dose = 150 # nA*sec

# Define the materials
k411 = epq.Material(epq.Composition([epq.Element.Ca,epq.Element.Fe,epq.Element.O,
                                     epq.Element.Mg, epq.Element.Si],
                                    [0.112, 0.112, 0.429, 0.092, 0.256] ),
                                    epq.ToSI.gPerCC(2.95))
k411.setName("SRM-2066")
c = epq.MaterialFactory.createPureElement(epq.Element.C)

scale = (dose*1.0e-9) / (nTraj * epq.PhysicalConstants.ElectronCharge)

# Place the sample at the optimal location for the detector
origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())

def computeBulk(comp, e0):
    mc = nm.MonteCarloSS()
    mc.setBeamEnergy(epq.ToSI.keV(e0))
    gun=nm.GaussianBeam(1.0e-9)
    gun.setCenter([0.0,0.0,-0.01])
    mc.setElectronGun(gun)
    mc.addSubRegion(mc.getChamber(),comp,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0],origin))
    mc.addActionListener(nm.XRayEventListener2(mc,det))
    mc.addActionListener(nm.BremsstrahlungEventListener(mc,det))
    # Create a simulator and initialize it
    # Run the MC
    det.reset()
    mc.runMultipleTrajectories(nTraj)
    # Get the spectrum and assign properties
    res=det.getSpectrum(scale)
    props=res.getProperties()
    props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,comp.descriptiveString(false))
    props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
    props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
    props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
    path = "%s/E=%g keV" % (DefaultOutput, e0)
    jio.File(path).mkdirs()
    fos = jio.FileOutputStream("%s/Bulk[%s].msa" % (path, comp))
    noisy=epq.SpectrumUtils.addNoiseToSpectrum(res, 1.0)
    ept.WriteSpectrumAsEMSA1_0.write(res,fos,0)
    fos.close()
    return res

k = 1.41421356237

out = textFile("%s/output[E=%g keV].csv" % (DefaultOutput, e0))
 
header = "E0\tsize\tI"
for i in range(0,8):
   header = "%s\tShape" % header
   for elm in k411.getElementSet():
      header = "%s\t%s" % (header, elm.toAbbrev())
out.println(header)

header = "\t\t"
for i in range(0,8):
   header = "%s\t" % header
   for elm in k411.getElementSet():
       header = "%s\t%2.5g" % (header, k411.weightFraction(elm,true)*100.0)
out.println(header)
  
quant = epq.QuantifySpectrumUsingStandards(det, epq.ToSI.keV(e0))
for elm in k411.getElementSet():
    quant.addStandard(elm,k411,computeBulk(k411, e0))
rois = quant.getMissingReferences()
elms = ju.TreeSet()
for roi in rois:
    for elm in roi.getElementSet():
        elms.add(elm)
quant.addElementToStrip(epq.Element.C)
for elm in elms:
    ref = computeBulk(epq.Material(elm,epq.ToSI.gPerCC(4.0)), e0)
    for roi in rois:
        if roi.getElementSet().contains(elm):
            quant.addReference(roi, ref)
for size in [0.1e-6, 0.2e-6, 0.4e-6, 0.8e-6, 1.6e-6, 3.2e-6, 6.4e-6, 12.8e-6]:
     print "size -> %g" % (size*1.0e6)
     if terminated:
         break
     for i in range(0,101):
         print "%d of 100" % i
         if terminated:
             break
         if i==0:
             phi=0
             th=0
             psi=0
         else:
             phi = 0.5*jl.Math.random()*jl.Math.PI
             th = 2.0*jl.Math.random()*jl.Math.PI
             psi = jl.Math.PI*jl.Math.random()
         # Determine a bounding box for the cube
         pts = [[-0.5*size, -0.5*size, -0.5*size],
                [-0.5*size, -0.5*size,  0.5*size],
                [-0.5*size,  0.5*size, -0.5*size],
                [-0.5*size,  0.5*size,  0.5*size],
                [ 0.5*size, -0.5*size, -0.5*size],
                [ 0.5*size, -0.5*size,  0.5*size],
                [ 0.5*size,  0.5*size, -0.5*size],
                [ 0.5*size,  0.5*size,  0.5*size]]
         maxZ = [0.0,0.0,0.0]
         for pt in pts:
             r = epu.Transform3D.rotate(pt,phi,th,psi)
             for j in range(0,3):
                if r[j]>maxZ[j]:
                 maxZ[j]=r[j]

         path = "%s/E=%g keV/size=%g um" % (DefaultOutput, e0, size*1.0e6)
         jio.File(path).mkdirs()
         monte = nm.MonteCarloSS()
         gun=nm.OverscanElectronGun(2.0*maxZ[0],2.0*maxZ[1])
         gun.setCenter([0.0,0.0,-0.01])
         monte.setElectronGun(gun)
         monte.setBeamEnergy(epq.ToSI.keV(e0))
         # A cube of size randomly rotate by phi, th, psi
         center = epu.Math2.plus(origin,[0.0,0.0,-maxZ[2]])
         monte.addSubRegion(monte.getChamber(),k411,nm.MultiPlaneShape.createBlock([size, size, size],center,phi,th,psi))
         # Place it on a carbon substrate
         monte.addSubRegion(monte.getChamber(), c, nm.MultiPlaneShape.createBlock([1.0e-5,1.0e-5,1.0e-5],epu.Math2.plus(origin,[0.0,0.0,0.5e-5]),0.0,0.0,0.0) )
         # Add event listeners to model characteristic radiation
         xrel=nm.XRayEventListener2(monte,det)
         monte.addActionListener(xrel)
         brem=nm.BremsstrahlungEventListener(monte,det)
         monte.addActionListener(brem)
         # Create a simulator and initialize it
         # Run the MC
         det.reset()
         monte.runMultipleTrajectories(nTraj)
         # Dump geometry to VRML file
         pw=jio.PrintWriter("%s/Iter[%i].wrl" % (path, i))
         vrml=nm.TrajectoryVRML(monte,pw)
         vrml.renderSample()
         vrml.addView("Top",epu.Math2.plus(origin,[0.0,0.0,-1.0e-5]),[0.0,0.0,1.0])
         vrml.addView("Bottom",epu.Math2.plus(origin,[0.0,0.0,2.0e-5]),[0.0,0.0,-1.0])
         vrml.addView("X Side",epu.Math2.plus(origin,[-2.0e-5,0.0,0.0]),[1.0,0.0,0.0])
         vrml.addView("Y Side",epu.Math2.plus(origin,[0.0, -2.0e-5,0.0]),[0.0,1.0,0.0])
         pw.close()
         # Get the spectrum and assign properties
         spec=det.getSpectrum(scale)
         props=spec.getProperties()
         props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
         props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
         props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)

         # Write the spectrum to disk and display
         fos = jio.FileOutputStream("%s/Iter[%d].msa" % (path, i))
         noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec, 1.0)
         ept.WriteSpectrumAsEMSA1_0.write(spec,fos,0)
         fos.close()
         # keep the volume constant... 
         s1 = jl.Math.pow(1.0/jl.Math.PI,1.0/3.0)*size
         s2 = jl.Math.pow(1.5/jl.Math.PI,1.0/3.0)*size
         s3 = jl.Math.pow(0.75/jl.Math.PI,1.0/3.0)*size
         s4 = jl.Math.pow(2.0,1.0/3.0)*size
         shapes = [ epq.SampleShape.Bulk(), 
                   epq.SampleShape.Cylinder(s1,s1),
                   epq.SampleShape.Fiber(s1,s1),
                   epq.SampleShape.Hemisphere(s2),
                   epq.SampleShape.RightRectangularPrism(size,size,size),
                   epq.SampleShape.Sphere(s3),
                   epq.SampleShape.SquarePyramid(2.0*size),
                   epq.SampleShape.TetragonalPrism(s4,s4),
                   epq.SampleShape.TriangularPrism(s4,s4) ]
         str = "%g\t%s\t%d" % (e0, size, i)
         try:
             for sh in shapes:
                dup=epq.SpectrumUtils.copy(spec)
                dup.getProperties().setSampleShape(epq.SpectrumProperties.SampleShape,sh)
                dup.getProperties().setNumericProperty(epq.SpectrumProperties.SpecimenDensity,2.95)
                q=quant.compute(dup)
                str = "%s\t%s" % (str, sh)
                for elm in k411.getElementSet():
                   str = "%s\t%g" % (str,100.0*(q.weightFraction(elm,true)-k411.weightFraction(elm,true)))
             out.println(str)
         except:
            out.println("%d failed")
