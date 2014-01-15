# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-16
#
#  Modifications
#   Date      Who                       What
# ----------  ---  -------------------------------------------------
# 2014-01-11  JRM  added measProbeCurrentFromCu

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
import java.io as jio
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
  
def measProbeCurrentFromCu(thisCu, stdCu, det, e0, digits=4):
  """measProbeCurrentFromCu(thisCu, stdCu, det, e0, digits=4)
  Measure the probe current for a session spectrum (thisCu) from
  the Cu standard (a probe current proxy) relative to the reference
  spectrum (stdCu) spectrum used to record standards. This assumes
  a detector (det) and e0 kV. The results are rounded to the desired digits.
  We use the Cu lines.
  
  Returns a dictionary:
  pcMu  - the mean relative probe current (mean K-ratio for optimum TS)
  pcSE  - the standard error for the relative probe current
  optTS - the optimal transition set for this kV
  ffMet - the filter fit metric, close to 0 is good, close to 1 is bad.
  
  An example:
  import dtsa2.jmGen as jmg
  res = jmg.measProbeCurrentFromCu(unCuSpc, rfCuSpc, det, e0)
  """
  qa = epq.CompositionFromKRatios()
  ff = epq.FilterFit(det,epq.ToSI.keV(e0))
  ff.addReference(dt2.element("Cu"),stdCu)
  krs = ff.getKRatios(thisCu)
  opt = krs.optimalDatum(dt2.element("Cu"))
  optTS = opt.toString()
  ku=krs.getKRatioU(opt)
  pcMu = round(ku.doubleValue(), digits)
  pcSE = round(ku.uncertainty(), digits)
  ffMet = round(ff.getFitMetric(thisCu), digits)
  # return a dictionary
  ret = {"pcMu": pcMu, "pcSE": pcSE, "optTS": optTS, "ffMet": ffMet }
  return ret
  
def avgSpectra(dir, names, det, e0, wrkDist, pc=1, acqTime=100, resName="Avg", debug=False):
  """avgSpectra(dir, names, det, e0, wrkDist, pc=1, acqTime=100, resName="Avg", debug=False)
  Compute the average spectrum from a list (names) of file names, assuming the individuals
  were recorded with an acquisition time of (acqTime) sec using the detector (det)
  at e0 kV with a working distance (wrkDist) and a probe current (pc) with default 1 .
  Return return the average spectrum
  with a display (resName). The (debug) flag prints file names if positive.
  
  Example:
  import dtsa2.jmGen as jmg
  findDetector("FEI FIB620 EDAX-RTEM")
  theAvg = jmg.avgSpectra('C:\Temp\', ['Cu-12-1.spc','Cu-12-2.spc','Cu-12-3.spc'], det, 12, 17.1, 1.0, resName="Cu Std 12 kV")
  display(theAvg)
  """
  if(debug):
    print(names)
  nSpec = len(names)
  factor = 1.0 / float(nSpec)
  sPath = dir+names[0]
  sum  = dt2.wrap(ept.SpectrumFile.open(sPath)[0])
  updateCommonSpecProps(sum, det, name="", liveTime=acqTime, probeCur=pc, e0=e0, wrkDist=wrkDist)
  for i in range(1, nSpec):
    sPath = dir+names[i]
    tmp = dt2.wrap(ept.SpectrumFile.open(sPath)[0])
    updateCommonSpecProps(tmp, det, name="", liveTime=acqTime, probeCur=pc, e0=e0, wrkDist=wrkDist)
    sum += tmp
  avg=factor*sum
  updateCommonSpecProps(avg, det, name=resName, liveTime=acqTime, probeCur=pc, e0=e0, wrkDist=wrkDist)
  return avg

def makeStdSpcSpectra(prjBaseDir, stdName, nDupl, vkV, det, wrkDist, pc=1, acqTime=100, debug=False):
  """ makeStdSpcSpectra(prjBaseDir, stdName, nDupl, vkV, det, wrkDist, pc=1, acqTime=100, debug=False)
  Generate standard spectra for a project with base directory (prjBaseDir) for
  the standard with (stdName) from (nDupl) duplicate spectra recorded at
  each of a list (vkV) of accelerating voltages with detector (det), working
  distance (wrkDist), and probe current (pc, default 1.0) and acquisition time (acqTime, default 100 sec).
  A debug flag(default, False) prints names.
  This assumes EDAX spc spectra
  are all store in prjBaseDir with names of the form stdName-12-1.spc where
  12 is the kV and 1 is the duplicate number. This writes the standards in
  files like prjBaseDir/msa/std/12kV/stdName.msa.
  
  Example:
  import dtsa2.jmGen as jmg
  findDetector("FEI FIB620 EDAX-RTEM")
  vkV = [10, 12, 15, 20, 25, 30]
  prjBaseDir = 'C:/Temp'
  makeStdSpcSpectra(prjBaseDir, "Cu", 3, vkV, det, 17.1, 1.0, 100.0, False)
  """
  for e0 in vkV:
    vNames = []
    disName='%s Std %gkV' % (stdName, e0)
    spcDir = prjBaseDir + '/spc/stds/'
    msaDir = prjBaseDir + '/msa/std/%gkV/' % e0
    for i in range(nDupl):
      vNames.append('%s-%g-%d.spc' % (stdName, e0, i+1))
    if(debug):
      print(vNames)
    
    theAvg = avgSpectra(spcDir, vNames, det, e0, wrkDist, pc, acqTime, resName=disName, debug=debug)
    updateCommonSpecProps(theAvg, det, name=disName, liveTime=acqTime, probeCur=pc, e0=e0, wrkDist=wrkDist)
    dt2.display(theAvg)
    
    outFil = msaDir + '%s.msa' % stdName
    a = glob.glob(outFil)
    if (len(a) > 0):
      os.remove(a[0])
    fos=jio.FileOutputStream(outFil)
    ept.WriteSpectrumAsEMSA1_0.write(theAvg,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
    fos.close()
    if(debug):
      print(outFil)
      
def getSpcAcqTime(spc):
  """getSpcAcqTime(spc)
  Return a string representation of the the local acquisition date and time for the input spectrum.
  Example:
  import dtsa2.jmGen as jmg
  strTim = jmg.getSpcAcqTime(cuSpc)
  """
  props = spc.getProperties()
  ts = props.getTimestampProperty(epq.SpectrumProperties.AcquisitionTime)
  acqTim = ts.toLocaleString()
  return acqTim
 