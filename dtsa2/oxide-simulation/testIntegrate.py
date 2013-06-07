# testIntegrate.py
#
import os

def myPeakIntegral(spect, kev, widEv, digits=1):
	ev = 1000*kev
	hw = 0.5*widEv
	start = ev - hw
	end = ev + hw
	res = epq.SpectrumUtils.backgroundCorrectedIntegral(spect, start, end)
	r0 = round(res[0],digits)
	r1 = round(res[1],digits)
	# r0  = '%.0f' % res[0]
	# r1  = '%.0f' % res[1]
	ret = [r0, r1]
	return ret
	
home=os.environ['HOME']
# home=home+"/"

# relative path to the spectrum
rel="/git/dtsa2/DemoSpectra/Benitoite/Al2O3 std.msa"
sFile=home+rel

spec = readSpectrum(sFile)
# N.B. this seems to be required to get this to work
spec.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)

display(spec)
sw=wrap(spec)
oPk = myPeakIntegral(sw.wrapped, 0.5249, 250)
print oPk
alPk = myPeakIntegral(sw.wrapped, 1.486, 250)
print alPk

