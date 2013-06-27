def createContaminatedDetector(det, tIce=0, tOil=0, e0=200):
  """createContaminatedDetector(det, tIce)
  Create a contamination detector with an ice layer tIce microns and an
  oil layer tOil microns to respond to a beam energy of e0 kV from the
  input detector (det)"""
  detNew = det
  dp=detNew.getDetectorProperties().getProperties()
  dp.setNumericProperty(epq.SpectrumProperties.IceThickness, tIce)
  dp.setNumericProperty(epq.SpectrumProperties.OilThickness, tOil)
  dp.setNumericProperty(epq.SpectrumProperties.BeamEnergy,epq.ToSI.keV(e0))
  detNew.setOwner(det.getOwner())
  return detNew


# wd = windowTransmission(d2)
# wd.display()
  
d = det=findDetector("FEI CM20UT EDAX-RTEM")

dNew = createContaminatedDetector(d, tIce=10000, tOil=0, e0=200)
wn = windowTransmission(dNew)
wn.display()
