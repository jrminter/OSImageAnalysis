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


import dtsa2 as dt2
import dtsa2.mcSimulate3 as mc3
import dtsa2.jmGen as jmg

"""A series of wrapper scripts to make Monte Carlo simulation
of Ni on Cu on PET spectra easier.
Place this file in DTSA_ROOT/lib/dtsa2/  call with
import dtsa2.mcNiCu as mcNiCu"""

def simNiCuPetSpc(tNi, tCu, e0, det, wkDst=17, lt=100, pc=1, nTraj=1000):
  """simNiCuPetSpc(tNi, tCu, e0, det, wkDst=17, lt=100, pc=1, nTraj=1000)
  Simulate a spectrum from tNi nm of Ni on tCu nm of Cu on PET recoreded at
  e0 kV using the DTSA detector det and a wkDst mm working distance for
  lt sec with a probe current of pc nA. Compute nTraj trajectories."""
  tPET = 76 # um
  pet = dt2.material("C10H8O4",density=1.37)
  cu  = dt2.material("Cu", density=8.96)
  ni  = dt2.material("Ni", density=8.90)
  lNi   = [ni,  tNi*1.0e-9]
  lCu   = [cu,  tCu*1.0e-9]
  lPET  = [pet, tPET*1.0e-6]
  lay   = [lNi, lCu, lPET]
  sNam  = "%g-nm-Ni-%g-nm-Cu-on-PET-%g-kV" % (tNi, tCu, e0)
  spc = dt2.wrap(mc3.multiFilm(lay, det, e0, True, nTraj, lt*pc, True, True))
  props=spc.getProperties()
  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, sNam)
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  props.setNumericProperty(epq.SpectrumProperties.WorkingDistance, wkDst)
  return(spc)
  
def anaMcNiCuKa(spc, det, stdBase, maxCh=1200):
  props=spc.getProperties()
  e0 = props.getNumericProperty(epq.SpectrumProperties.BeamEnergy)
  lt = props.getNumericProperty(epq.SpectrumProperties.LiveTime)
  pc = props.getNumericProperty(epq.SpectrumProperties.FaradayBegin)
  wkDst = props.getNumericProperty(epq.SpectrumProperties.WorkingDistance)
  spc = jmg.cropSpec(spc, end=maxCh)
  unSpc = jmg.updateCommonSpecProps(spc, det, liveTime=lt, probeCur=pc, e0=e0, wrkDist=wkDst)
  dt2.display(unSpc)
  
  # define the transitions I want to measure
  tsNiKa = epq.XRayTransitionSet(epq.Element.Ni, epq.XRayTransitionSet.K_FAMILY)
  tsCuKa = epq.XRayTransitionSet(epq.Element.Cu, epq.XRayTransitionSet.K_FAMILY)
  trs = [tsNiKa, tsCuKa]
  relStd = "/%gkV/" % (e0)
  stdDir = stdBase + relStd
  niFile = stdDir + "Ni-sim.msa"
  cuFile = stdDir + "Cu-sim.msa"

  spc = dt2.wrap(ept.SpectrumFile.open(niFile)[0])
  props=spc.getProperties()
  e0 = props.getNumericProperty(epq.SpectrumProperties.BeamEnergy)
  lt = props.getNumericProperty(epq.SpectrumProperties.LiveTime)
  pc = props.getNumericProperty(epq.SpectrumProperties.FaradayBegin)
  wkDst = props.getNumericWithDefault(epq.SpectrumProperties.WorkingDistance, wkDst)
  spc = jmg.cropSpec(spc, end=maxCh)
  niSpc = jmg.updateCommonSpecProps(spc, det, liveTime=lt, probeCur=pc, e0=e0, wrkDist=wkDst)
  dt2.display(niSpc)

  spc = dt2.wrap(ept.SpectrumFile.open(cuFile)[0])
  props=spc.getProperties()
  e0 = props.getNumericProperty(epq.SpectrumProperties.BeamEnergy)
  lt = props.getNumericProperty(epq.SpectrumProperties.LiveTime)
  pc = props.getNumericProperty(epq.SpectrumProperties.FaradayBegin)
  wkDst = props.getNumericWithDefault(epq.SpectrumProperties.WorkingDistance, wkDst)
  spc = jmg.cropSpec(spc, end=maxCh)
  cuSpc = jmg.updateCommonSpecProps(spc, det, liveTime=lt, probeCur=pc, e0=e0, wrkDist=wkDst)
  dt2.display(cuSpc)
  niStd = {"El":dt2.element("Ni"), "Spc":niSpc}
  cuStd = {"El":dt2.element("Cu"), "Spc":cuSpc}
  stds  = [niStd, cuStd]
  theKR = jmg.compKRs(unSpc, stds, trs, det, e0)
  krNiCalc = theKR[0]
  krCuCalc = theKR[1]
  return [krNiCalc, krCuCalc]
  
def compKrRmsDev(expl, modl):
  """compKrRmsDev(expl, modl)
  Compute the rms deviation between lists of experimental and model
  K-ratios. Return -1 if the lists are not the same length"""
  l1 = len(expl)
  l2 = len(modl)
  if(l1 != l2):
    # not the same length, an error
    return(-1)
  i = 0
  rmsDev = 0
  while(i < l1):
    delta = modl[i] - expl[i]
    rmsDev += math.sqrt(delta*delta)
    i += 1
  return(rmsDev)
    
  
  

