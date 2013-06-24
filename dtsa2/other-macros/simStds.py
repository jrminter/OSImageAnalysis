# simStds.py
# simulate Ni and Cu stds
#
#
import os
import sys
import shutil

home=os.environ['HOME']
# the project directory
proj=home+"/work/proj/tst/"

# relative path to where we want to store the data
rel="dat/dtsa-sim/std/"
base=proj+rel
pyRept=proj + "py/simStds Results/"



det=findDetector("FEI620-EDAX RTEM")
e0=15 # keV
nTraj=10000 # electrons
dose=150 # nA*sec

Ni=epq.MaterialFactory.createPureElement(epq.Element.Ni)
Cu=epq.MaterialFactory.createPureElement(epq.Element.Cu)

stds=[Ni, Cu]
names=["Ni", "Cu"]

for i in range(len(stds)):
  # place sample at optimal location for the detector
  origin=epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))
  # create a simulator and initialze initialize it.

  monte=nm.MonteCarloSS()
  monte.setBeamEnergy(epq.ToSI.keV(e0))

  # create the substrate
  monte.addSubRegion(monte.getChamber(),stds[i],nm.MultiPlaneShape.createSubstrate([ 0.0, 0.0, -1.0],origin))

  # add event listener to model characteristic radiation
  xrel=nm.XRayEventListener2(monte,det)
  monte.addActionListener(xrel)
  brem=nm.BremsstrahlungEventListener(monte,det)
  monte.addActionListener(brem)
  
  det.reset()
  monte.runMultipleTrajectories(nTraj)
  # Get the spectrum and properties
  spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
  props=spec.getProperties()

  props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,
  "%s-sim-std" % names[i])
  props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
  props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)

  # Write to disk and display
  fos=jio.FileOutputStream("%s%s-sim-std.msa" % (base, names[i]) )
  noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
  ept.WriteSpectrumAsEMSA1_0.write(noisy,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
  fos.close()
  display(noisy)
  
# clean up cruft
shutil.rmtree(pyRept)
print "Done!"

