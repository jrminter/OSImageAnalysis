# simCuOstd.py
# simulate a 50 nm CuO films
#
# should just need to change nmThick...
# and base path for a system
#
import os
home=os.environ['HOME']
home=home+"/"

nmThick=50


# relative path to where we want to store the data
rel="/work/proj/QM13-02-05D-Irving/dat/dtsa-sim/std/"
base=home+rel


det=findDetector("EDAX RTEM")
e0=200 # keV
nTraj=10000 # electrons
dose=150 # nA*sec
layThick=nmThick*1.0e-9 # 
cThick= 50.0e-9 # 50 nm

# density from http://en.wikipedia.org/wiki/Copper(II)_oxide

cuo=epq.Material(epq.Composition([epq.Element.Cu, epq.Element.O],
[0.798865,0.201135]), epq.ToSI.gPerCC(6.31))

# place sample at optimal location for the detector
origin=epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))

# create a simulator and initialze initialize it.

monte=nm.MonteCarloSS()
monte.setBeamEnergy(epq.ToSI.keV(e0))

# create the film
lay=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, 0.0], layThick)

monte.addSubRegion(monte.getChamber(),cuo,lay)


# add event listener to model characteristic radiation
xrel=nm.XRayEventListener2(monte,det)
monte.addActionListener(xrel)
ei=nm.EmissionImage.watchDefaultTransitions(xrel, 512, 2*layThick, origin)
# add event listener to model bremsstrahlung
brem=nm.BremsstrahlungEventListener(monte,det)
monte.addActionListener(brem)

# reset the detector and run the trajectories
det.reset()
monte.runMultipleTrajectories(nTraj)
# Get the spectrum a	properties
spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge))
props=spec.getProperties()


props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName,
"%gnm-CuO-std" % nmThick)
props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)



# Write to disk and display
fos=jio.FileOutputStream("%s/CuO-%gnm-std.msa" % (base, nmThick))
noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
# ept.WriteSpectrumAsEMSA1_0.write(noisy,fos,0)
fos.close()
display(noisy)
# nm.Emissionlmage.dumpToFiles(ei,"%s/R=%g nm images" % (DefaultOutput, layThick)
