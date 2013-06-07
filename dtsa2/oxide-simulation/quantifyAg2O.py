# quantifyAg2O.py

# Local system configuration options
import os, math

def anaCOAg(spect, digits=5):
	sw=wrap(spect)
	res = epq.SpectrumUtils.backgroundCorrectedIntegral(sw.wrapped, 203, 377)
	cPkMu = round(res[0],1)
	cPkSe = round(res[1],1)
	res = epq.SpectrumUtils.backgroundCorrectedIntegral(sw.wrapped, 421, 639)
	oPkMu = round(res[0],1)
	oPkSe = round(res[1],1)
	res = epq.SpectrumUtils.backgroundCorrectedIntegral(sw.wrapped, 2511, 3934)
	agPkMu = round(res[0],1)
	agPkSe = round(res[1],1)
	cAgMu = cPkMu/agPkMu
	cAgSe=cAgMu*math.sqrt((cPkSe/cPkMu)**2+(agPkSe/agPkMu)**2)
	# C/Ag
	r1 = round(cAgMu, digits)
	r2 = round(cAgSe, digits)
	oAgMu = oPkMu/agPkMu
	oAgSe = oAgMu*math.sqrt((oPkSe/oPkMu)**2+(agPkSe/agPkMu)**2)
	# O/Ag
	r3 = round(oAgMu, digits)
	r4 = round(oAgSe, digits)
	ret = [sw.wrapped.toString(), r1, r2, r3, r4]
	return ret


home=os.environ['HOME']
home=home+"/"

# Find the detector...
det=findDetector("EDAX RTEM")
e0=200 # keV
print "Using detector: %s" % det.toString()

# relative path to where we store the unknowns
relUnk="/work/proj/QM13-02-05D-Irving/dat/dtsa-sim/msa/"
# unkfDir is the location of the references
unkDir = home+relUnk

sd=ept.SpectrumFile.open("%s/Ag2O50nm-on-50nm-C.msa" % unkDir, )[0]
sd.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
display(sd)

ratio1 = anaCOAg(sd, digits=8)

sd2=ept.SpectrumFile.open("%s/Ag2O1000nm-on-50nm-C.msa" % unkDir, )[0]
sd2.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
display(sd2)

ratio2 = anaCOAg(sd2, digits=8)

sd3=ept.SpectrumFile.open("%s/Ag2O10000nm-on-50nm-C.msa" % unkDir, )[0]
sd3.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
display(sd3)

ratio3 = anaCOAg(sd3, digits=8)

print(ratio1)
print(ratio2)
print(ratio3)
