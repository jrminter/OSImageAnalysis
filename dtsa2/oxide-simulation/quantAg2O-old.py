# quantAgO.py

# Local system configuration options
import os
home=os.environ['HOME']
home=home+"/"


# relative path to where we store the standards
relStd="/work/proj/QM13-02-05D-Irving/dat/dtsa-sim/std/"

# refDir is the location of the references
refDir = home+relStd

cuo = ept.SpectrumFile.open("%s%s" % (refDir, "CuO-50nm-std.msa"))[0]
cuo.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
ag = ept.SpectrumFile.open("%s%s" % (refDir, "Ag-50nm-std.msa"))[0]
ag.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)

# Find the detector...
det=findDetector("EDAX RTEM")
e0=200 # keV
print "Using detector: %s" % det.toString()

ff=epq.FilterFit(det,epq.ToSI.keV(e0))
ff.addReference(element("O"),cuo)
ff.addReference(element("Ag"),ag)

# relative path to where we store the unknowns
relUnk="/work/proj/QM13-02-05D-Irving/dat/dtsa-sim/msa/"
# unkfDir is the location of the references
unkDir = home+relUnk

sd=ept.SpectrumFile.open("%s/Ag2O50nm-on-50nm-C.msa" % unkDir, )[0]
sd.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
display(sd)
kr=ff.getKRatios(sd)
kO=kr.getKRatioU(epq.XRayTransition(epq.Element.O,epq.XRayTransition.KA1))
kAg=kr.getKRatioU(epq.XRayTransition(epq.Element.Ag,epq.XRayTransition.LA1))
print kO
print kAg


