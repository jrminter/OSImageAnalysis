# anaRaw.py
#
# Analyze the EDS spectra from the "as-received" specimen of
# PMH1332 (qm-03868). This should be essentially pure Ag. We
# integrate the overlap region between Ag/Cl and the strongest
# Ag peak and write the integrals to a comma-delimited file.
#
import os
import sys

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
imgRoot=os.environ['IMG_ROOT']
# home=home+"/"
print home

strOutFile = home + "/work/proj/QM13-02-10A-Wang/dat/csv/qm-03868-PMH1332-rp2-int.csv"

# relative path to the spectrum
rel="QM13-02-10A-Wang/qm-03868-PMH1332-rp2/spc/"
theSpec="qm-03868-pmh1332-rp2-02a.spc"

ClMu = []
ClSe = []
AgMu = []
AgSe = []

iCount=0
path=imgRoot+rel
for file in os.listdir(path):
	sFile = os.path.join(path, file)
	spec = readSpectrum(sFile)
	# N.B. this seems to be required to get this to work
	spec.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
	display(spec)
	sw=wrap(spec)
	ClPk = myPeakIntegral(sw.wrapped, 2.660, 180)
	ClMu.append(ClPk[0])
	ClSe.append(ClPk[1])
	AgPk = myPeakIntegral(sw.wrapped, 2.994, 180)
	AgMu.append(AgPk[0])
	AgSe.append(AgPk[1])
	clear()
	iCount += 1

f=open(strOutFile, 'w')
strLine = 'i, Cl.Mu, Cl.SE, Ag.Mu, Ag.SE\n'
f.write(strLine)
for i in range(iCount):
	strLine = "%d" % i + ","
	strLine = strLine + "%.2f" % ClMu[i] + ","
	strLine = strLine + "%.2f" % ClSe[i] + ","
	strLine = strLine + "%.2f" % AgMu[i] + ","
	strLine = strLine + "%.2f" % AgSe[i] + "\n"
	f.write(strLine)  
f.close()


