# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-15

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


import dtsa2 as dt2

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