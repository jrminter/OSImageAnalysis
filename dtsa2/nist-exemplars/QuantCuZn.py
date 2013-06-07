# A script for extracting k-ratios.  Written for Jeff Davis to 
# process data from an XRF linescan.
# Nicholas W. M. Ritchie

# Local system configuration options
# refDir is the location of the references
refDir = "S:/JeffDavis/Cu-Zn Linescans/"

cu = ept.SpectrumFile.open("%s%s" % (refDir, "Cu standard.spc"))[0]
cu.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
zn = ept.SpectrumFile.open("%s%s" % (refDir, "Zn standard.spc"))[0]
zn.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
# Find the detector...
det = Database.findDetector("e2v 12.8")
print "Using detector: %s" % det.toString()

ff=epq.FilterFit(det,epq.ToSI.keV(40))
ff.addReference(element("Cu"),cu)
ff.addReference(element("Zn"),zn)

print "Cu\td(Cu)\tZn\td(Zn)"
for n in range(251,376):
    sd=ept.SpectrumFile.open("%s/LinescanA%d.spc" % (refDir, n))[0]
    sd.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
    kr=ff.getKRatios(sd)
    kCu=kr.getKRatioU(epq.XRayTransition(epq.Element.Cu,epq.XRayTransition.KA1))
    kZn=kr.getKRatioU(epq.XRayTransition(epq.Element.Zn,epq.XRayTransition.KA1))
    print "%g\t%g\t%g\t%g" % (kCu.doubleValue(), kCu.uncertainty(), kZn.doubleValue(), kZn.uncertainty())

print "Done!"