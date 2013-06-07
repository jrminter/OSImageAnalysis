# -*- coding: utf-8 -*-
# DTSA-II/NISTMonte script - Nicholas W. M. Ritchie - 6-May-2010
"""A series of script for simulating various common geometries using the 3rd generation NISTMonte Monte Carlo simulation algorithms.
Note that the Monte Carlo algorithm requires densities for all materials.  Usually this is accomplished by:
  1) creating a epq.Material object directly
  2) using createMaterial(...)
  3) using the material(str,density) version of the material utility function
The methods basically implement the same geometries as the GUI but facilitate scripting multiple simulations.
Methods:
   mcSimulate(mat, [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [xtraParams])
   mcSphere(mat, [radius], [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [substrate], [xtraParams])
   mcMultiFilm(layers, [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [xtraParams])
   mcEmbeddedSphere(mat, radius, substrate, depth, [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [xtraParams])   
   mcEmbeddedRectangle(mat, dims, substrate, depth, [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [xtraParams]):
   mcInterface(primary, offset, secondary, [det], [e0], [withPoisson], [nTraj], [dose], [sf], [bf], [xtraParams])
Internal methods: (for special customization)    
   mcBase(det, e0, withPoisson, nTraj, dose, sf, bf, name, buildSample, buildParams, xtraParams)
xtraParams:
   xtraParams is a mechanism to allow for flexible yet efficient generation of alternative output mechanisms such as emission images, accumulators and phi(rho*z) curves.
   Emission images: xtraParams = { 
      'Transitions' : [list of XRayTransitions], 
      'Emission Images' : double(dimension of image in meters) }
   Characteristic Accumulator: xtraParams = { 
      'Transitions' : [list of XRayTransitions],
      'Characteristic Accumulator' : True }
   Bremstrahling Fluorescence Accumulator: xtraParams = { 
      'Transitions' : [list of XRayTransitions],
      'Brem Fluor Accumulator' : True }
   Characteristic Fluorescence Accumulator: xtraParams = { 
      'Transitions' : [list of XRayTransitions],
      'Char Fluor Accumulator' : True }
   Phi(rho*z): xtraParams = { 'PhiRhoZ' : double(depth dimension in meters) }"""

print """mcSimulate3 - Scripts to facilitate Monte Carlo simulation
   help(mcSimulate3) for documentation"""

# Example:
# 1> xp = { "Transitions" : [transition("Fe K-L3"), transition("Fe K-M3"), transition("Fe L3-M5"), transition("O K-L3")], "Emission Images":5.0e-6, "Characteristic Accumulator":True, "Char Fluor Accumulator":True, "Brem Fluor Accumulator":True, "PhiRhoZ":5.0e-6, "Output" : "Z:/nritchie/Desktop/tmp" }
# 2> display(mcSimulate(material("Fe2O3",5.0), d2, 20.0, nTraj=100, sf=True, bf=True, xtraParams = xp))

# Mac OS X seems to require the next line.
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3, FluorescenceXRayGeneration3, XRayTransport3", None)
import gov.nist.microanalysis.NISTMonte.Gen3 as nm3

import epq.base

def mcBase(det, e0, withPoisson, nTraj, dose, sf, bf, name, buildSample, buildParams, xtraParams):
   """mcBase(det,e0,withPoisson, nTraj, dose, sf, bf, name, buildSample, buildParams) represents
   a generic mechanism for Monte Carlo simulation of x-ray spectra.  The argument buildSample
   is a method buildSample(monte,origin,buildParams) taking an instance of MonteCarloSS, the 
   position of the origin and a dictionary of build parameters.  This method should construct
   the sample geometry.  The other arguments are the detector, the beam energy (keV), whether
   to add Poisson noise, the number of electron trajectories to simulate, whether to simulate
   characteristic secondary fluorescence and Bremsstrahlung secondary fluorescence, the name
   to assign to the resulting spectrum."""
   if e0<0.1:
       raise "The beam energy must be larger than 0.1 keV."
   if nTraj<1:
       raise "The number of electron trajectories must be larger than or equal to 1."
   if dose<=0.0:
       raise "The electron dose must be larger than zero."
   name=name.strip()
   # Place the sample at the optimal location for the detector
   origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())
   detPos = epq.SpectrumUtils.getDetectorPosition(det.getProperties())
   # Create a simulator and initialize it
   monte = nm.MonteCarloSS()
   monte.setBeamEnergy(epq.ToSI.keV(e0))
   buildSample(monte,origin,buildParams)
   # Add event listeners to model characteristic radiation
   chXR = nm3.CharacteristicXRayGeneration3.create(monte)
   xrel=nm3.XRayTransport3.create(monte, det, chXR)
   brXR = nm3.BremsstrahlungXRayGeneration3.create(monte)
   brem=nm3.XRayTransport3.create(monte, det, brXR)
   if sf:
      chSF=nm3.XRayTransport3.create(monte, det, nm3.FluorescenceXRayGeneration3.create(monte, chXR))
   if bf:    
      brSF=nm3.XRayTransport3.create(monte, det, nm3.FluorescenceXRayGeneration3.create(monte, brXR))
   if xtraParams.has_key("Transitions"):
       if xtraParams.has_key("Emission Images"):
           eis=[]
           dim = xtraParams["Emission Images"]
           for xrt in xtraParams["Transitions"]:
               ei=nm3.EmissionImage3(512,512,xrt)
               xrel.addXRayListener(ei)
               if chSF:
                   chSF.addXRayListener(ei)
               if brSF:
                   brSF.addXRayListener(ei)
               ei.setXRange(origin[0]-0.5*dim,origin[0]+0.5*dim)
               ei.setYRange(origin[2]-0.1*dim,origin[2]+0.9*dim)
               eis.append(ei)
       if xtraParams.has_key("Characteristic Accumulator"):
           cxra=nm3.XRayAccumulator3(xtraParams["Transitions"])
           xrel.addXRayListener(cxra)
       if xtraParams.has_key("Char Fluor Accumulator") and sf:
           cfxra=nm3.XRayAccumulator3(xtraParams["Transitions"])
           chSF.addXRayListener(cfxra) 
       if xtraParams.has_key("Brem Fluor Accumulator") and bf:
           bfxra=nm3.XRayAccumulator3(xtraParams["Transitions"])
           brSF.addXRayListener(bfxra)
   if xtraParams.has_key("PhiRhoZ"):
       depth=xtraParams["PhiRhoZ"]
       prz=nm3.PhiRhoZ3(xrel,origin[2]-0.1*depth, origin[2]+1.1*depth,110)
       xrel.addXRayListener(prz)
   # Reset the detector and run the electrons
   det.reset()
   monte.runMultipleTrajectories(nTraj)
   # Get the spectrum and assign properties
   spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge) )
   props=spec.getProperties()
   props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
   props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
   props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
   epq.SpectrumUtils.renameSpectrum(spec,name)
   if withPoisson:
      spec=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
   defOut=(globals()['DefaultOutput'] if globals().has_key('DefaultOutput') else ("%s/Results" % sys.currentWorkingDir))
   do = "%s/%s" % ((xtraParams["Output"] if xtraParams.has_key("Output") else defOut),name)
   jio.File(do).mkdirs()
   if xtraParams.has_key("Transitions"):
      pw=None
      if xtraParams.has_key("Characteristic Accumulator") or (xtraParams.has_key("Brem Fluor Accumulator") and bf) or (xtraParams.has_key("Char Fluor Accumulator") and sf):
         pw=jio.PrintWriter("%s/Intensity.csv" % do)
         pw.println(name)
      if xtraParams.has_key("Characteristic Accumulator"):
         pw.println("Characteristic") 
         cxra.dump(pw)
      if xtraParams.has_key("Brem Fluor Accumulator") and bf:
         pw.println("Bremsstrahlung Fluorescence")
         bfxra.dump(pw)
      if xtraParams.has_key("Char Fluor Accumulator") and sf:
         pw.println("Characteristic Fluorescence")
         cfxra.dump(pw)
      if pw:
          pw.close()
      if xtraParams.has_key("Emission Images"):
         tmp="%s/%s" % (do, name)
         jio.File(tmp).mkdirs()
         nm3.EmissionImage3.dumpToFiles(eis,tmp)
   if xtraParams.has_key("PhiRhoZ"):
       pw=jio.PrintWriter("%s/%s[PhiRhoZ].csv" % (do, name))
       prz.write(pw)
       pw.close()
   return wrap(spec)

def mcSimulate(mat, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, xtraParams = {}):
   """mcSimumate(mat,det,[e0=20.0],[withPoisson=True],[nE=1000],[sf=False],[bf=False] - Simulate a bulk spectrum for the material mat on the
   detector det at beam energy e0 (in keV).  If sf then simulate characteristic secondary fluorescence.
   If bf then simulate bremsstrahlung secondary fluorescence. nTraj specifies the number of electron trajectories.
   dose is in nA*sec.
   """
   def buildBulk(monte,origin,buildParams):
      mat = buildParams["Material"]
      monte.addSubRegion(monte.getChamber(),mat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], origin) )
   tmp="MC simulation of bulk %s%s%s " % (mat,(" + CSF" if sf else ""),(" + BSF" if bf else ""))
   res = mcBase(det, e0, withPoisson, nTraj, dose, sf, bf, tmp, buildBulk, { "Material" : mat }, xtraParams)
   res.getProperties().setCompositionProperty(epq.SpectrumProperties.StandardComposition,mat)
   return res
   
   
def mcSphere(mat, radius, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, substrate=None, xtraParams = {}):
   """mcSphere(mat, radius, det, [e0=20.0], [withPoisson=True], [nTraj=1000], [dose = 120.0], [sf=False], [bf=False], [substrate=None])
   Monte Carlo simulate a spectrum from a spherical particle of the specified material (mat) and radius (in m).
   If substrate != None then substrate specifies the Material for an infinitely thick substrate immediately
   below the particle."""
   if radius<0.0:
       raise "The sphere radius must be larger than zero."
   def buildSphere(monte,origin,buildParams):
      radius=buildParams["Radius"]
      subMat=buildParams["Substrate"]
      mat = buildParams["Material"]
      sphere=nm.Sphere(epu.Math2.plus(origin,[0.0,0.0,radius]),radius)
      monte.addSubRegion(monte.getChamber(),mat,sphere)
      if subMat:
         monte.addSubRegion(monte.getChamber(),subMat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], epu.Math2.plus(origin,[0.0,0.0,2.0*radius])) )
   tmp = "MC simulation of a %0.2f µm sphere of %s%s%s%s" % (radius*1.0e6, mat,(" on %s" % substrate if substrate else ""),(" + CSF" if sf else ""),(" + BSF" if bf else ""))
   return mcBase(det,e0,withPoisson,nTraj,dose,sf,bf,tmp,buildSphere,{"Substrate": substrate, "Radius" : radius, "Material" : mat}, xtraParams)


def mcMultiFilm(layers, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, xtraParams = {}):
   """mcMultiFilm(layers, det, [e0=20.0], [withPoisson=True], [nTraj=1000], [dose = 120.0], [sf=False], [bf=False]):
   Monte Carlo simulate a spectrum from a multilayer thin film.  Layers is a iterable list of 
   [material,thickness]. Note the materials must have associated densities."""
   def buildFilm(monte,origin,buildParams):
      sr=monte.getChamber()
      for layer in buildParams["Layers"]:
          if layer[1]<=0.0:
              raise "The layer thickness must be larger than zero."
          sr=monte.addSubRegion(sr,layer[0],nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0],origin))
          origin=epu.Math2.plus(origin,[0.0,0.0,layer[1]])
      sr=monte.addSubRegion(sr,epq.Material.Null,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0],origin))
   tmp = "MC simulation of a multilayer film [%s]%s%s" % (",".join("%0.2f um of %s" % (1.0e6*layer[1],layer[0]) for layer in layers),(" + CSF" if sf else ""),(" + BSF" if bf else ""))
   return mcBase(det,e0,withPoisson,nTraj,dose,sf,bf,tmp, buildFilm,{"Layers": layers }, xtraParams)
               
         
def mcEmbeddedSphere(mat, radius, substrate, depth, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, xtraParams = {}):
   """mcEmbeddedSphere(mat, radius, substrate, depth, det, [e0=20.0], [withPoisson=True], [nTraj=1000], [dose = 120.0], [sf=False], [bf=False], [substrate=None])
   Monte Carlo simulate a spectrum from a spherical particle of the specified material (mat) and radius (in m)
   embedded in a substrate (Material) at depth (in m)."""
   if depth<0.0:
       raise "The depth parameter must be greater than zero."
   if radius<0.0:
       raise "The sphere radius must be larger than zero."
   def buildEmbeddedSphere(monte,origin,buildParams):
      mat = buildParams["Material"]
      radius=buildParams["Radius"]
      subMat=buildParams["Substrate"]
      depth=buildParams["Depth"]
      sr=monte.addSubRegion(monte.getChamber(),subMat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], origin) )
      monte.addSubRegion(sr,mat,nm.Sphere(epu.Math2.plus(origin,[0.0,0.0,depth+radius]),radius))
   tmp = "MC simulation of a %0.2f µm sphere of %s embedded %0.2f µm in %s%s%s" % (radius*1.0e6, mat, depth*1.0e6, substrate,(" + CSF" if sf else ""),(" + BSF" if bf else ""))
   return mcBase(det,e0,withPoisson,nTraj,dose,sf,bf,tmp,buildEmbeddedSphere,{"Substrate": substrate, "Radius" : radius, "Depth" : depth, "Material" : mat}, xtraParams)

def mcEmbeddedRectangle(mat, dims, substrate, depth=0.0, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, xtraParams = {}):
    """mcEmbeddedRectangle(mat, dims, substrate, depth=0.0, det, [e0=20.0], [withPoisson=True], [nTraj=1000], [dose = 120.0], [sf=False], [bf=False])"""
    if isinstance(dims,float):
        dims=[dims,dims,dims]
    def buildEmbeddedRectange(monte, origin, buildParams):
        mat=buildParams["Material"]
        subMat=buildParams["Substrate"]
        dims=buildParams["Dimension"]
        depth=buildParams["Depth"]
        sr=monte.addSubRegion(monte.getChamber(),subMat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], origin) )
        pos = epu.Math2.plus(origin,[0.0,0.0,0.5*dims[2]+depth])
        monte.addSubRegion(sr,mat,nm.MultiPlaneShape.createBlock(dims,pos,0.0,0.0,0.0))
    tmp = "MC simulation of a [%0.2f µm,%0.2f µm,%0.2f µm] block of %s embedded %0.2f µm in %s%s%s" % (dims[0], dims[1], dims[2], mat, depth*1.0e6, substrate,(" + CSF" if sf else ""),(" + BSF" if bf else ""))
    return mcBase(det,e0,withPoisson,nTraj,dose,sf,bf,tmp,buildEmbeddedRectange,{"Substrate": substrate, "Dimension" : dims, "Depth" : depth, "Material" : mat}, xtraParams)
      

def mcInterface(primary, offset, secondary, det, e0=20.0, withPoisson=True, nTraj=1000, dose = 120.0, sf=False, bf=False, xtraParams = {}):
   """mcInterface(mat, radius, substrate, depth, det, [e0=20.0], [withPoisson=True], [nTraj=1000], [dose = 120.0], [sf=False], [bf=False], [substrate=None])
   Monte Carlo simulate a spectrum from a spherical particle of the specified material (mat) and radius (in m)
   embedded in a substrate (Material) at depth (in m)."""
   def buildInterface(monte,origin,buildParams):
      mat = buildParams["Material"]
      secondary=buildParams["Secondary"]
      offset=buildParams["Offset"]
      dim=0.001
      dims=[dim,dim,dim]
      cp = epq.Math2.plus(origin,[-0.5*dim+offset,0.0,0.5*dim])
      cs = epq.Math2.plus(origin,[0.5*dim+offset,0.0,0.5*dim])
      monte.addSubRegion(monte.getChamber(),mat,nm.MultiPlaneShape.createBlock(dims,cp,0.0,0.0,0.0))
      monte.addSubRegion(monte.getChamber(),secondary,nm.MultiPlaneShape.createBlock(dims,cs,0.0,0.0,0.0))
   tmp = "MC simulation of a probe placed in %s %0.2f µm from %s" % (primary, offset, secondary,(" + CSF" if sf else ""),(" + BSF" if bf else ""))
   return mcBase(primary,det,e0,withPoisson,nTraj,dose,sf,bf,tmp,buildInterface, {"Secondary" : secondary, "Offset" : offset, "Material" : mat}, xtraParams)
