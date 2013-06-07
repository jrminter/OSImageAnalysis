# DTSA-II/NISTMonte script - Nicholas W. M. Ritchie - 17-Sep-2008
# A basic script for simulating a bulk material

# Identify a user defined detector and initialize configuration parameters
det = findDetector("Bruker 5")
e0 = 15 # keV
nTraj = 100 # electrons
dose = 150 # nA*sec

# Define the materials
mat = epq.Material(epq.Composition([epq.Element.Ca,epq.Element.Fe,epq.Element.O,
                                     epq.Element.Al,epq.Element.Mg, epq.Element.Si],
                                    [0.1090, 0.0774, 0.4276, 0.0491, 0.1166, 0.2120] ),
                                    epq.ToSI.gPerCC(5.0))

# Place the sample at the optimal location for the detector
origin = epq.SpectrumUtils.getSamplePosition(det.getProperties())
detPos = epq.SpectrumUtils.getDetectorPosition(det.getProperties())

# Create a simulator and initialize it
monte = nm.MonteCarloSS()
monte.setBeamEnergy(epq.ToSI.keV(e0))

monte.addSubRegion(monte.getChamber(),mat,nm.MultiPlaneShape.createSubstrate([0.0,0.0,-1.0], origin) )
# Add event listeners to model characteristic radiation

xrel=nm.XRayTransport.create(monte, det, chXR = nm.CharacteristicXRayGeneration.create(monte))
brem=nm.XRayTransport.create(monte, det, brXR = nnm.BremsstrahlungXRayGeneration.create(monte))
if 0:
    chSF=nm.XRayTransport.create(monte, det, nnm.FluorescenceXRayGeneration.create(monte, chXR))
    brSF=nm.XRayTransport.create(monte, det, nnm.FluorescenceXRayGeneration.create(monte, brXR))

ei=nm.EmissionImage.watchDefaultTransitions(xrel, 512, 4.0e-6, origin)
if 0:
    cfi=nm.EmissionImage.watchDefaultTransitions(chSF, 512, 40.0e-6, origin)
    bfi=nm.EmissionImage.watchDefaultTransitions(brSF, 512, 40.0e-6, origin)

# Reset the detector and run the electrons
det.reset()
monte.runMultipleTrajectories(nTraj)
# Get the spectrum and assign properties
spec=det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge) )
props=spec.getProperties()
props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, 
                  "%g micron sphere with 10 nm Gold coating on C substrate" % (r/1.0e-6))
props.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
props.setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
props.setNumericProperty(epq.SpectrumProperties.BeamEnergy,e0)
# Write the spectrum to disk and display
fos = jio.FileOutputStream("%s/R = %g um.msa" % (DefaultOutput, r/1.0e-6))
noisy=epq.SpectrumUtils.addNoiseToSpectrum(spec,1.0)
ept.WriteSpectrumAsEMSA1_0.write(noisy,fos,0)
fos.close()
display(noisy)
nm.EmissionImage.dumpToFiles(ei,"%s/R = %g um images" % (DefaultOutput, r/1.0e-6))