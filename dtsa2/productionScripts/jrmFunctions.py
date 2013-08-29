# jrmFunctions.py
# John Minter's DTSA-II Jython Script Functions
# Licensed under the GPL2 | BSD License
# Version 0.9.3  2013-08-29 - added function compPhiRhoZ
# Version 0.9.2  2013-08-23 - added function anaNiCuKRimpW
# Version 0.9.1  2013-07-11 - cleans up after loading
# Version 0.9.0  2013-06-26 - initial release
#

import os
import sys
import shutil

gitDir=os.environ['GIT_HOME']
relDir="/OSImageAnalysis/dtsa2/productionScripts"
pyrDir="./jrmFunctions Results"

curDir=os.getcwd()

wd=gitDir+relDir
os.chdir(wd)


# Define functions

def compPhiRhoZ(comp, det, e0, nSteps=100, simple=True, outdir="./"):
  """compPhiRhoZ(comp, det, e0, nSteps=100, simple=True, outdir="./")
  Computes the ionization  as a function of dept for the composition
  (comp) with the specified detector (det) with the specified number
  of steps (nSteps). If simple is true, the XPP1991 algorithm is
  used, otherwise the full PAP1991 algorithm is used. The results
  are written to a .csv file in the output directory (outdir)
  Example:
  e0     =  25
  nSteps = 200
  cu     = material("Cu", density=8.96)
  det    = findDetector("FEI FIB620 EDAX-RTEM")
  compPhiRhoZ(cu, det, e0, nSteps, simple=True, outdir="c:/temp/")
  """
  sName = comp.getName()
  if(simple == True):
    alg = epq.XPP1991()
    sFile = "%s-xpp-prz-%g-kv" % (sName, e0)
  else:
    alg = epq.PAP1991()
    sFile = "%s-pap-prz-%g-kv" % (sName, e0)
  print "Computing " + sFile
  fName = outdir + sFile + ".csv"
  fi = open(fName,'w')
  sp = epq.SpectrumProperties(det.getProperties())
  sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  xrts = majorTransitions(comp, e0)
  rhoZmax = epq.ElectronRange.KanayaAndOkayama1972.compute(comp, epq.ToSI.keV(e0))
  res = "Idx,rhoz(mg/cm^2)"
  for xrt in xrts:
    res = "%s,G(%s),E(%s)" % (res, xrt, xrt)
  res = res + "\n"
  fi.write(res)
  for step in range(0, nSteps):
    rz = step * rhoZmax / nSteps
    res = "%d,%g" % (step, 100.0 * rz) # in mg/cm^2
    for xrt in xrts:
      alg.initialize(comp, xrt.getDestination(), sp)
      res = "%s,%g,%g" % (res, alg.computeCurve(rz), alg.computeAbsorbedCurve(xrt, rz))
    res=res+"\n"
    fi.write(res)
  fi.close()

def anaNiCuKR(unSpec, niSpec, cuSpec, det, e0):
  """anaNiCuKR(unSpec, niSpec, cuSpec, det, e0)
  analyze the K-Ratios for Ni and Cu from unknown (unSpec) spectrum using
  standard spectra niSpec and cuSpec recorded from the detector identified
  by the string (det) at an accelerating voltage (e0) kV. Returns a list
  with the unknown name ('name') and the K-Ratios ('Ni' and 'Cu'). 
  
  Example:
  theKR = anaNiCuKR(unSpc, niSpc, cuSpc, "FEI FIB620 EDAX-RTEM", 15.0)
  """
  # first, prepare the spectra
  sw=wrap(unSpec)
  unSpec=sw
  sw=wrap(niSpec)
  niSpec = sw
  sw=wrap(cuSpec)
  cuSpec = sw
  # Now set up the calc
  xrtsNi = epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.K_FAMILY)
  xrtsCu = epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.K_FAMILY)
  qa = epq.CompositionFromKRatios()
  det = Database.findDetector(det)
  ff=epq.FilterFit(det,epq.ToSI.keV(e0))
  ff.addReference(element("Ni"),niSpec)
  ff.addReference(element("Cu"),cuSpec)
  # get the k-ratios from the unknown
  krs=ff.getKRatios(unSpec)
  krNi=krs.getKRatio(xrtsNi)
  krCu=krs.getKRatio(xrtsCu)
  name=unSpec.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  return {'name': name, 'Ni': krNi, 'Cu': krCu}

def anaNiCuKRimpW(unSpec, niSpec, cuSpec, wSpec, det, e0):
  """anaNiCuKRimpW(unSpec, niSpec, cuSpec, wSpec, det, e0)
  analyze the K-Ratios for Ni and Cu from unknown (unSpec) spectrum in the
  presence of W impurity using standard spectra niSpec, cuSpec, and wSpec
  recorded from the detector identified by the string (det) at an accelerating
  voltage (e0) kV. Returns a list with the unknown name ('name') and the
  K-Ratios ('Ni' and 'Cu'). 
  
  Example:
  theKR = anaNiCuKRimpW(unSpc, niSpc, cuSpc, wSpec, "FEI FIB620 EDAX-RTEM", 15.0)
  """
  # first, prepare the spectra
  sw=wrap(unSpec)
  unSpec=sw
  sw=wrap(niSpec)
  niSpec = sw
  sw=wrap(cuSpec)
  cuSpec = sw
  sw=wrap(wSpec)
  wSpec = sw
  # Now set up the calc
  xrtsNi = epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.K_FAMILY)
  xrtsCu = epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.K_FAMILY)
  qa = epq.CompositionFromKRatios()
  det = Database.findDetector(det)
  ff=epq.FilterFit(det,epq.ToSI.keV(e0))
  ff.addReference(element("Ni"),niSpec)
  ff.addReference(element("Cu"),cuSpec)
  ff.addReference(element("W"),wSpec)
  # get the k-ratios from the unknown
  krs=ff.getKRatios(unSpec)
  krNi=krs.getKRatio(xrtsNi)
  krCu=krs.getKRatio(xrtsCu)
  name=unSpec.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  return {'name': name, 'Ni': krNi, 'Cu': krCu}


def clearAllSpectra():
  """clearAllSpectra()
  Clear all spectra from the data manager. Loaded from jrmFunctions.py."""
  DataManager = dt2.DataManager.getInstance()
  DataManager.clearSpectrumList()

def compPeakIntegral(spect, kev, widEv, digits=1):
  """compPeakIntegral( spect, kev, widEv, digits=1)
  Compute the background-corrected peak interval for the line at kev keV with an
  integration width of widEv eV and return the results the desired (typically 1)
  following the decimal. Loaded from jrmFunctions.py."""
  ev = 1000*kev
  hw = 0.5*widEv
  start = ev - hw
  end = ev + hw
  res = epq.SpectrumUtils.backgroundCorrectedIntegral(spect, start, end)
  r0 = round(res[0],digits)
  r1 = round(res[1],digits)
  # note: under the hood, this returns the estimate, res[0] 
  # and the uncertainty, res[1]. Typically it is one digit.
  # r0  = '%.0f' % res[0]
  # r1  = '%.0f' % res[1]
  ret = [r0, r1]
  return ret


def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it.
  Loaded from jrmFunctions.py."""
  if not os.path.exists(d):
    os.makedirs(d)

def getKalphaEnergy(elmName):
  """getKalphaEnergy("Cu")
  Returns the transition energy (in keV) for the element's K-alpha
  line as the weighted sum of Ka1 and Ka2. Loaded from jrmFunctions.py."""
  elm = element(elmName)
  xrt = epq.XRayTransition.KA1
  try:
    if epq.XRayTransition.exists(elm, xrt):
      tr = epq.XRayTransition(elm, xrt)
      en1 = epq.FromSI.keV(tr.getEnergy())
      wt1 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      xrt = epq.XRayTransition.KA2
      tr = epq.XRayTransition(elm, xrt)
      en2 = epq.FromSI.keV(tr.getEnergy())
      wt2 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      en = (wt1*en1+wt2*en2)/(wt1+wt2)
      return round(en, 4) 
    else:
      print "invalid element"
      return -1.0
  except jl.IllegalArgumentException:
    pass

def getLalphaEnergy(elmName):
  """getLalphaEnergy("Cu")
  Returns the transition energy (in keV) for the element's L-alpha line as
  the weighted sum of La1 and La2. Loaded from jrmFunctions.py."""
  elm = element(elmName)
  xrt = epq.XRayTransition.LA1
  try:
    if epq.XRayTransition.exists(elm, xrt):
      tr = epq.XRayTransition(elm, xrt)
      en1 = epq.FromSI.keV(tr.getEnergy())
      wt1 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      xrt = epq.XRayTransition.LA2
      tr = epq.XRayTransition(elm, xrt)
      en2 = epq.FromSI.keV(tr.getEnergy())
      wt2 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      en = (wt1*en1+wt2*en2)/(wt1+wt2)
      return round(en, 4) 
    else:
      print "invalid element"
      return -1.0
  except jl.IllegalArgumentException:
    pass

def getKLenergy(elmName):
  """getKLenergy(elmName)
  returns the weighted energy (in keV) for the element's K-alpha and
  L-alpha lines as a dictionary. Loaded from jrmFunctions.py."""
  enK = getKalphaEnergy(elmName)
  enL = getLalphaEnergy(elmName)
  res = {"K-alpha" : enK, "L-alpha" : enL}
  return res

def renameSpec(spc, newName):
  """renameSpec(spc, newName)
  change the name of a current spectrum to newName
  """
  spc.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, newName)
  spc=wrap(spc)
  return spc

def spcTopHatFilter(spc, det, e0, fw=150, norm=False):
  """spcTopHatFilter(spc, det, e0, fw=150, norm=False)
  Compute a top hat filter for spectrum spc with the given detector
  the specified kV (e0) with the desired filter width and normalization.
  Loaded from jrmFunctions.py.
  """
  rawName=spc.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  fltName=rawName+"-thf"
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin, 1.0)
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  sw=wrap(spc)
  spc=sw
  thf=epq.FittingFilter.TopHatFilter(fw, det.getChannelWidth())
  fs=epq.FilteredSpectrum(spc, norm)
  fs.setFilter(thf)
  fs.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, fltName)
  fsw=wrap(fs)
  return fsw
  
def simBrehmTEM(det, e0, matl, matlThick, subMat, subThick, nTraj=10000, dose=150, addNoise=True):
  """simBrehmTEM(det, e0, matl, matlThick, subMat, subThick, nTraj=10000, dose=150, addNoise=True)
  Simulate the bremsstrahlung continuum spectrum for the detector (det),
  at the accelerating voltage (e0) keV, for the DTSA material (matl) with
  thickness (matlThick) in nm on the substrate DTSA material (subMat) with
  thickness (subThick) in nm by computing nTraj trajectories assuming a dose
  (dose, in nA) and if desired, (addNoise) simulating a noisy spectrum.
  
  An example:
  det=findDetector("FEI CM20UT EDAX-RTEM")
  # create materials
  ago=epq.Material(epq.Composition([epq.Element.Ag, epq.Element.O],[0.930958,0.069042]), epq.ToSI.gPerCC(7.14))
  c=epq.MaterialFactory.createPureElement(epq.Element.C)
  brehm = simBrehmTEM(det, 200.0, ago, 200.0, c, 50.0, nTraj=10000, dose=150, addNoise=True)
  display(brehm)
  """
  layTh=matlThick*1.0e-9
  subTh=subThick*1.0e-9
  # create a simulator and initialze initialize it.
  monte=nm.MonteCarloSS()
  monte.setBeamEnergy(epq.ToSI.keV(e0))
  # create the film
  lay=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, 0.0], layTh)
  # create the substrate
  sub=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0,layTh], subTh)
  monte.addSubRegion(monte.getChamber(),matl,lay)
  monte.addSubRegion(monte.getChamber(),subMat,sub)
  # add event listener to model bremsstrahlung
  brem=nm.BremsstrahlungEventListener(monte,det)
  monte.addActionListener(brem)
  # reset the detector and run the trajectories
  det.reset()
  monte.runMultipleTrajectories(nTraj)
  spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
  props=spec.getProperties()
  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,"Computed brehmstrahlung (%g nm matl, %g nm sub)" % (matlThick, subThick))
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
  if(addNoise==True):
    noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
    noisy.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,"Computed noisy brehmstrahlung (%g nm matl, %g nm sub)" % (matlThick, subThick))
    return wrap(noisy)
  else:
    return wrap(spec)

  
  

# clean up cruft
shutil.rmtree(pyrDir)
# back where we started
os.chdir(curDir)
