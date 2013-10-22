# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-16

import sys
import os
import glob
import shutil
import time
import math
import csv

sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3, FluorescenceXRayGeneration3, XRayTransport3", None)
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.NISTMonte.Gen3 as nm3
import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import gov.nist.microanalysis.Utility as epu
import gov.nist.microanalysis.EPQTools as ept
import java.lang as jl


import dtsa2 as dt2
import dtsa2.mcSimulate3 as mc3

"""A series of wrapper scripts to make DTSA-II automation easy
Place this file in DTSA_ROOT/lib/dtsa2/  call with
import dtsa2.jmGen as jmg"""

def isNaN(num):
  """isNaN(num)
  Check if a number is NaN, returning True of False"""
  return num != num

def checkNaN(x):
  """checkNaN(x)
  This checks if a value (e.g. K-ratio) is NaN and sets the value to
  zero if it is. This really helps when writing data frames to be
  read by R."""
  if isNaN(x):
    x = 0.0
  return x
  
def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)
    
def clearAllSpectra():
  """clearAllSpectra()
  Clear all spectra from the data manager. Loaded from jrmFunctions.py."""
  DataManager = dt2.DataManager.getInstance()
  DataManager.clearSpectrumList()
  
def compPeakIntegral(spc, e0, wid, digits=1):
  """compPeakIntegral( spc, e0, wid, digits=1)
  Compute the background-corrected peak interval for the line at e0 keV with an
  integration width of wid eV and return the results the desired (typically 1)
  following the decimal."""
  ev = 1000*e0
  hw = 0.5*wid
  start = ev - hw
  end = ev + hw
  res = epq.SpectrumUtils.backgroundCorrectedIntegral(spc, start, end)
  r0 = round(res[0],digits)
  r1 = round(res[1],digits)
  # note: under the hood, this returns the estimate, res[0] 
  # and the uncertainty, res[1]. Typically it is one digit.
  # r0  = '%.0f' % res[0]
  # r1  = '%.0f' % res[1]
  ret = [r0, r1]
  return ret
  
def updateCommonSpecProps(spc, det, name="", liveTime=-1, probeCur=-1, e0=-1, wrkDist=-1):
  """updateCommonSpecProps(spc, det, name="", liveTime=-1, probeCur=-1, e0=-1, wrkDist=-1)
  Update common spectrum properties
  spc      - the spectrum (must supply)
  det      - the detector (must supply)
  name     - display name (will update if not empty)
  liveTime - acquisition live time (sec) (will update if > 0)
  probeCur - probe current (in nA) (will update if > 0)
  e0       - incident beam energy (in kV) (will update if > 0)
  wrkDist  - working distance (in mm) (will update if > 0)
  This is helpful if they were not set properly in a GUI..."""
  props=spc.getProperties()
  props.setDetector(det)
  l = len(name)
  if(l > 0) :
    props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, name)
  if(liveTime > 0) :
    props.setNumericProperty(epq.SpectrumProperties.LiveTime, liveTime)
  if(probeCur > 0) :
    props.setNumericProperty(epq.SpectrumProperties.FaradayBegin, probeCur)
  if(e0 > 0) :
    props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  if(wrkDist > 0) :
    props.setNumericProperty(epq.SpectrumProperties.WorkingDistance, wrkDist)
  return spc

def compKRs(unSpc, stds, trs, det, e0, digits=5):
  """compKRs(unSpc, stds, trs, det, e0, digits=5)
  Peforms a MLLSQ filter-fit of unknown spectrum (unSpc),
  to the standard spectra in a list of dictionaries of standards.
  Each standard in the list is a dictionary like
  {"El":element("C"), "Spc":cSpc} containing the element name
  and the standard spectrum. The function then computes the
  k-ratios for a list of transition sets (trs). The
  function returns a list of k-ratios, rounded to the desired
  number of digits. The function performs an NaN test, setting
  NaNs to zero."""
  # Now set up the calc
  qa = epq.CompositionFromKRatios()
  ff=epq.FilterFit(det,epq.ToSI.keV(e0))
  l = len(stds)
  for i in range(0, l):
    st=stds[i]
    el=st["El"]
    sp=st["Spc"]
    ff.addReference(el,sp)
  krs=ff.getKRatios(unSpc)
  kr=[]
  n = len(trs)
  for i in range(0, n):
    tr=trs[i]
    k=round(checkNaN(krs.getKRatio(tr)), digits)
    kr.append(k)
  return kr

def cropSpec(spc, start=0, end=2048):
  """cropSpec(spc, start=0, end=2048)
  crop the spectrum (spc) starting with a starting and ending channel.
  This transfers the channel width, zero offset, and probe current
  required for microanalysis.
  
  Example:
  import dtsa2.jmGen as jmg
  niSpc = ept.SpectrumFile.open(niFile)[0]
  niSpc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
  ws = wrap(niSpc)
  niSpc = jmg.cropSpec(ws, end=maxCh)
  """
  dt2.display(spc)
  nm = spc.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  dt2.clear()
  cw = spc.getChannelWidth()
  zo = spc.getZeroOffset()
  lt = spc.liveTime()
  pc = spc.probeCurrent()
  cr = epq.SpectrumUtils.slice(spc, start, end)
  sp = epq.SpectrumUtils.toSpectrum(cw, zo, end, cr)
  sp = dt2.wrap(sp)
  sp.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, nm)
  dt2.display(sp)
  sp.setProbeCurrent(pc)
  sp.setLiveTime(lt)
  dt2.DataManager.removeSpectrum(spc)
  return sp

def getKalphaEnergy(elmName):
  """getKalphaEnergy("Cu")
  Returns the transition energy (in keV) for the element's K-alpha
  line as the weighted sum of Ka1 and Ka2."""
  elm = dt2.element(elmName)
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
  elm = dt2.element(elmName)
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

def simBulkSpcCor(name, matl, det, e0=15, nTraj=100, lt=100, pc=1, noise=True):
  """simBulkSpcCor(name, matl, det, e0=15, nTraj=100, lt=100, pc=1, noise=True)
  Use the mc3 Monte Carlo functions to simulate bulk spectrum from a material with a live time lt
  and a probe current pc at a voltage e0. This does corrects for continuum fluorescence.
  Example:
  import dtsa2.jmGen as jmg
  det=findDetector("FEI FIB620 EDAX-RTEM")
  ni = material("Ni", density=8.90)
  niSpc = jmg.simBulkSpcCor("Ni-sim", ni, det, e0=15,nTraj=100, lt=60, pc=1)
  display(niSpc)
  """
  
  dose = lt*pc
  spc = dt2.wrap(mc3.simulate(matl, det, e0, True, nTraj, dose, True, True))
  props = spc.getProperties()
  sName = "%s-%gkV" % (name, e0)

  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, sName)
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
  return spc

def simBulkSpcUnCor(name, matl, det, e0=15, nTraj=100, lt=100, pc=1, noise=True):
  """simBulkSpcUnCor(name, matl, det, e0=15, nTraj=100, lt=100, pc=1, noise=True)
  Use the standard Monte Carlo functions to simulate bulk spectrum from a material with a live time lt
  and a probe current pc at a voltage e0.
  This does not correct for continuum fluorescence.
  Example:
  import dtsa2.jmGen as jmg
  det=findDetector("FEI FIB620 EDAX-RTEM")
  ni = material("Ni", density=8.90)
  niSpc = jmg.simBulkSpcUnCor("Ni-sim", ni, det, e0=15,nTraj=100, lt=60, pc=1)
  display(niSpc)
  """
  origin=epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))
  # create a simulator and initialize initialize it.

  monte=nm.MonteCarloSS()
  monte.setBeamEnergy(epq.ToSI.keV(e0))

  # create the substrate
  monte.addSubRegion(monte.getChamber(),matl,nm.MultiPlaneShape.createSubstrate([ 0.0, 0.0, -1.0],origin))

  # add event listener to model characteristic radiation
  xrel=nm.XRayEventListener2(monte,det)
  monte.addActionListener(xrel)
  brem=nm.BremsstrahlungEventListener(monte,det)
  monte.addActionListener(brem)
  
  det.reset()
  monte.runMultipleTrajectories(nTraj)
  # Get the spectrum and properties
  dose = lt*pc
  spc=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
  if noise:
    spc=epq.SpectrumUtils.addNoiseToSpectrum(spc,1.0)
  props=spc.getProperties()
  sName="%s-%gkV" % (name, e0)

  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, sName)
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
  return spc

def spcTopHatFilter(spc, det, e0, fw=150, norm=False):
  """spcTopHatFilter(spc, det, e0, fw=150, norm=False)
  Compute a top hat filter for spectrum spc with the given detector
  the specified kV (e0) with the desired filter width and normalization.
  """
  rawName=spc.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  fltName=rawName+"-thf"
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin, 1.0)
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  sw=dt2.wrap(spc)
  spc=sw
  thf=epq.FittingFilter.TopHatFilter(fw, det.getChannelWidth())
  fs=epq.FilteredSpectrum(spc, norm)
  fs.setFilter(thf)
  fs.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, fltName)
  fsw=dt2.wrap(fs)
  return fsw
  
def compPhiRhoZ(comp, det, e0, nSteps=100, alg=epq.PAP1991(), base="pap-prz", outdir="./"):
  """compPhiRhoZ(comp, det, e0, nSteps=100, alg=epq.PAP1991(), base="pap-prz", outdir="./")
  Computes the ionization  as a function of dept for the composition
  (comp) with the specified detector (det) with the specified number
  of steps (nSteps). Algorithm choices are, the epq.XPP1991()
  (simplified Pouchou), epq.PAP1991() (full Pouchou and Pichoir)
  or epq.Proza96Base() (Bastin et al) algorithms. The results
  are written to a .csv file in the output directory (outdir)
  Example:
  import dtsa2.jmGen as jmg
  e0     =  25
  nSteps = 200
  cu     = material("Cu", density=8.96)
  det    = findDetector("FEI FIB620 EDAX-RTEM")
  jmg.compPhiRhoZ(cu, det, e0, nSteps, alg=epq.XPP1991(), base="xpp-prz", outdir="c:/temp/")
  """
  sName = comp.getName()
  sFile = "%s-%s-%g-kv" % (sName, base, e0)
  print "Computing " + sFile
  fName = outdir + sFile + ".csv"
  fi = open(fName,'w')
  sp = epq.SpectrumProperties(det.getProperties())
  sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  xrts = dt2.majorTransitions(comp, e0)
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
  
def simMatlOnSubTEM(det, e0, matl, matlThick, subMat, subThick, lNames, nTraj=10000, lt=100, pc=1):
  """simMatlOnSubTEM(det, e0, matl, matlThick, subMat, subThick, lNames, nTraj=10000, lt=100, pc=1)
  Simulate a material on a thin substrate in the TEM for the detector (det),
  at the accelerating voltage (e0) keV, for the DTSA material (matl) with
  thickness (matlThick) in nm on the substrate DTSA material (subMat) with
  thickness (subThick) in nm with a list of names lNames = [matName, subName] by computing
  nTraj trajectories assuming a live time (lt, sec) and a probe current (pc, in nA) and
  simulating a noisy spectrum.
  Example:
  import dtsa2.jmGen as jmg
  det=findDetector("FEI CM20UT EDAX-RTEM")
  # create materials
  ago=epq.Material(epq.Composition([epq.Element.Ag, epq.Element.O],[0.930958,0.069042]), epq.ToSI.gPerCC(7.14))
  c=epq.MaterialFactory.createPureElement(epq.Element.C)
  spc = jmg.simMatlOnSubTEM(det, 200.0, ago, 100.0, c, 50.0, ["Ag2O","C"],  nTraj=10000, lt=100, pc=1)
  display(spc)
  """
  dose = lt*pc
  layTh=matlThick*1.0e-9
  subTh=subThick*1.0e-9
  # place sample at optimal location for the detector
  origin=epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))
  # create a simulator and initialize it.
  monte=nm.MonteCarloSS()
  monte.setBeamEnergy(epq.ToSI.keV(e0))
  # create the film
  lay=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, 0.0], layTh)
  # create the substrate
  sub=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0,layTh], subTh)
  monte.addSubRegion(monte.getChamber(), matl, lay)
  monte.addSubRegion(monte.getChamber(), subMat, sub)
  # add event listener to model characteristic radiation
  xrel=nm.XRayEventListener2(monte,det)
  monte.addActionListener(xrel)
  # ei=nm.EmissionImage.watchDefaultTransitions(xrel, 512, 2*layThick, origin)
  # add event listener to model bremsstrahlung
  brem=nm.BremsstrahlungEventListener(monte,det)
  monte.addActionListener(brem)
  # reset the detector and run the trajectories
  det.reset()
  monte.runMultipleTrajectories(nTraj)
  # Get the spectrum a	properties
  spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
  noisy=dt2.wrap(epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0))
  props=noisy.getProperties()
  spName = "Sim %g nm %s on %g nm %s" % (matlThick, lNames[0], subThick,  lNames[1])
  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, spName)
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
  return(noisy)
  
def simBrehmTEM(det, e0, matl, matlThick, subMat, subThick, lNames, nTraj=10000, lt=100, pc=1):
  """simBrehmTEM(det, e0, matl, matlThick, subMat, subThick, lNames, nTraj=10000, lt=100, pc=1)
  Simulate the bremsstrahlung continuum spectrum for the detector (det),
  at the accelerating voltage (e0) keV, for the DTSA material (matl) with
  thickness (matlThick) in nm on the substrate DTSA material (subMat) with
  thickness (subThick) in nm  a list of names lNames = [matName, subName] 
  by computing nTraj trajectories assuming a live time (lt, sec) and a probe
  current (pc, in nA) and if desired, (addNoise) simulating a noisy spectrum.
  
  An example:
  import dtsa2.jmGen as jmg
  det=findDetector("FEI CM20UT EDAX-RTEM")
  # create materials
  ago=epq.Material(epq.Composition([epq.Element.Ag, epq.Element.O],[0.930958,0.069042]), epq.ToSI.gPerCC(7.14))
  c=epq.MaterialFactory.createPureElement(epq.Element.C)
  brehm = jmg.simBrehmTEM(det, 200.0, ago, 200.0, c, 50.0, ["Ag2O","C"], nTraj=10000, lt=100, pc=1)
  display(brehm)
  """
  dose = lt*pc
  layTh=matlThick*1.0e-9
  subTh=subThick*1.0e-9
  # create a simulator and initialize initialize it.
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
  noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
  props=noisy.getProperties()
  spName = "Sim brehmstrahlung %g nm %s on %g nm %s" % (matlThick, lNames[0], subThick,  lNames[1])
  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, spName)
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  return dt2.wrap(noisy)