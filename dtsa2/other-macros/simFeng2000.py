# -*- coding: utf-8 -*-
#         1         2         3         4         5         6         7  
#123456789012345678901234567890123456789012345678901234567890123456789012
#
# simFeng2000.py
# simulate spectra to model Feng2000
#
#
import os
import shutil
import java.io as jio

def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)

def simSpecOnSub(mat, sub, tMat, tSub, det, e0, pc, lt, nTraj):
  """simSpecOnSub(mat, sub, tMat, tSub, det, e0, pc, lt, nTraj)
  mat = material, sub = substrate, tMat = thickness in nm,
  tSub = thickness in nm, det = detector, e0 = kv, pc = probe cur nA,
  lt = live time sec, nTraj = # trajectories.
  returns a scriptable spectrum"""
  sf = 1.0e-9 # scale factor nm -> m for DTSA-II units
  
  # place sample at optimal location for the detector
  origin = epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))
  # create a simulator and initialize initialize it.
  monte = nm.MonteCarloSS()
  monte.setBeamEnergy(epq.ToSI.keV(e0))
  # create the substrate
  subst = nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, -tSub*sf], tSub*sf)
  # create the film
  layer = nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, 0.0], tMat*sf)
  monte.addSubRegion(monte.getChamber(), mat, layer)
  monte.addSubRegion(monte.getChamber(), sub, subst)
  # add event listener to model characteristic radiation
  xrel = nm.XRayEventListener2(monte,det)
  monte.addActionListener(xrel)
  # add event listener to model bremsstrahlung
  brem = nm.BremsstrahlungEventListener(monte,det)
  monte.addActionListener(brem)
  # reset the detector and run the trajectories
  det.reset()
  monte.runMultipleTrajectories(nTraj)
  dose = pc * lt # nA sec
  # Get the spectrum and  properties
  spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
  noisy = wrap(epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0))
  props = noisy.getProperties()
  props.setDetector(det)
  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,
  "%g nm %s film on %g nm %s substrate" % (tMat, mat.getName(), tSub, sub.getName()))
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  noisy.setAsStandard(mat)
  return noisy


git = os.environ['GIT_HOME']
edsDir = os.environ['EDS_ROOT']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros"
os.chdir(wd)

pyrDir = wd + "/simFeng2000 Results/"
# relative path to where we want to store the data
rel = "/edsDir"
datDir = edsDir+rel
ensureDir(datDir)

det     = findDetector("FEI CM20UT EDAX-RTEM")
nmThLay =    20    # thickness of the material in nm
nmThC   =    50    # thickness of C substrate in sf
e0      =   200.0  # keV
nTraj   = 10000    # electron trajectories
probeC  =    1.0   # probe current (nA)
liveTim =   100.0  # sec

# start clean
DataManager.clearSpectrumList()

# materials to simulate
# density from Wikipedia unless otherwise noted
ag = epq.Material(epq.Composition([epq.Element.Ag], [1.0]), epq.ToSI.gPerCC(10.49))
s = epq.Material(epq.Composition([epq.Element.S], [1.0]), epq.ToSI.gPerCC(2.25))
c = epq.Material(epq.Composition([epq.Element.C], [1.0]), epq.ToSI.gPerCC(2.1))
oso2 = epq.Material(epq.Composition([epq.Element.Os, epq.Element.O], [0.8560, 0.1440]), epq.ToSI.gPerCC(11.40))
# common lead citrate ppt
pbco3 = epq.Material(epq.Composition([epq.Element.Pb, epq.Element.O, epq.Element.C], [0.7754, 0.1796, 0.0449]), epq.ToSI.gPerCC(6.582))
uo2 = epq.Material(epq.Composition([epq.Element.U, epq.Element.O], [0.8815, 0.1185]), epq.ToSI.gPerCC(10.97))

agSpc = simSpecOnSub(ag, c, nmThLay, nmThC, det, e0, probeC, liveTim, nTraj)
sName = "Ag on C"
agSpc.rename(sName)
display(agSpc)
fos = jio.FileOutputStream("%s/%s.msa" % (datDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(agSpc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

sSpc = simSpecOnSub(s, c, nmThLay, nmThC, det, e0, probeC, liveTim, nTraj)
sName = "S on C"
sSpc.rename(sName)
display(sSpc)
fos = jio.FileOutputStream("%s/%s.msa" % (datDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(sSpc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

oso2Spc = simSpecOnSub(oso2, c, nmThLay, nmThC, det, e0, probeC, liveTim, nTraj)
sName = "OsO2 on C"
oso2Spc.rename(sName)
display(oso2Spc)
fos = jio.FileOutputStream("%s/%s.msa" % (datDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(oso2Spc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

uo2Spc = simSpecOnSub(uo2, c, nmThLay, nmThC, det, e0, probeC, liveTim, nTraj)
sName = "UO2 on C"
uo2Spc.rename(sName)
display(uo2Spc)
fos = jio.FileOutputStream("%s/%s.msa" % (datDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(uo2Spc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

pbco3Spc = simSpecOnSub(pbco3, c, nmThLay, nmThC, det, e0, probeC, liveTim, nTraj)
sName = "PbCO3 on C"
pbco3Spc.rename(sName)
display(pbco3Spc)
fos = jio.FileOutputStream("%s/%s.msa" % (datDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(pbco3Spc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"



