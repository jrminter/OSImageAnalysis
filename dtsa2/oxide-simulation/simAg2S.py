# simAg2S.py
# simulate Ag2S on 50 nm of C
#
# should just need to change nmThick...
# and base path for a system
#
nmThick=10000
# define a base path
#
base="C:/Users/jrminter/Documents/work/dat/dtsa/sim/"




det=findDetector("EDAX RTEM")
e0=200 # keV
nTraj=10000 # electrons
dose=150 # nA*sec
layThick=nmThick*1.0e-9 # 
cThick= 50.0e-9 # 50 nm

ags=epq.Material(epq.Composition([epq.Element.Ag, epq.Element.S],
[0.870602,0.129398]), epq.ToSI.gPerCC(7.23))
c=epq.MaterialFactory.createPureElement(epq.Element.C)

# place sample at optimal location for the detector
origin=epu.Math2.multiply(1.0e-3, epq.SpectrumUtils.getSamplePosition(det.getProperties()))

# create a simulator and initialze initialize it.

monte=nm.MonteCarloSS()
monte.setBeamEnergy(epq.ToSI.keV(e0))

# create the substrate
sub=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, -cThick], cThick)
# create the film
lay=nm.MultiPlaneShape.createFilm([0.0, 0.0, -1.0],[0.0, 0.0, 0.0], layThick)

monte.addSubRegion(monte.getChamber(),ags,lay)
monte.addSubRegion(monte.getChamber(),c,sub)


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
"%g nm Ag2S film on 50 nm C substrate" % nmThick)
props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)



# Write to disk and display
fos=jio.FileOutputStream("%s/Ag2S%gnm-on-50nm-C.msa" % (base, nmThick))
noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
# ept.WriteSpectrumAsEMSA1_0.write(noisy,fos,0)
fos.close()
display(noisy)
# nm.Emissionlmage.dumpToFiles(ei,"%s/R=%g nm images" % (DefaultOutput, layThick)
