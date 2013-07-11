# ana03892.py
#
# Analyze the EDS spectra from the 30 min HCl treated specimen of
# PMH1332 after light treatment (qm-03892). 
# We integrate the overlap region between Ag/Cl and the strongest
# Ag peak and write the integrals to a comma-delimited file.
#
import os
import sys
import shutil
import fnmatch

homDir=os.environ['HOME']
imgRoot=os.environ['IMG_ROOT']
prjDir=homDir+"/work/proj/QM13-02-10A-Wang-rpt"


strOutFile = homDir + "/work/proj/QM13-02-10A-Wang-rpt/dat/csv/qm-03892-PMH1332-hcl-30-lt.csv"

# relative path to the spectrum
rel="/QM13-02-10A-Wang-dat/qm-03892-PMH1332-HCl-30m-lt/spc/"
pyrDir="./ana03892 Results"

wd=prjDir+"/py"
os.chdir(wd)

spNa = []
ClMu = []
ClSe = []
AgMu = []
AgSe = []

iCount=0
path=imgRoot+rel
for file in os.listdir(path):
  if fnmatch.fnmatch(file, '*.spc'):
    print file
    sFile = os.path.join(path, file)
    spNa.append(file)
    spec = readSpectrum(sFile)
    # N.B. this seems to be required to get this to work
    spec.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
    display(spec)
    sw=wrap(spec)
    ClPk = compPeakIntegral(sw.wrapped, 2.660, 180)
    ClMu.append(ClPk[0])
    ClSe.append(ClPk[1])
    AgPk = compPeakIntegral(sw.wrapped, 2.994, 180)
    AgMu.append(AgPk[0])
    AgSe.append(AgPk[1])
    clear()
    iCount += 1
    DataManager.removeSpectrum(spec)

f=open(strOutFile, 'w')
strLine = 'i, Cl.Mu, Cl.SE, Ag.Mu, Ag.SE, name\n'
f.write(strLine)
for i in range(iCount):
  j = i+1
  strLine = "%d" % j + ","
  strLine = strLine + "%.2f" % ClMu[i] + ","
  strLine = strLine + "%.2f" % ClSe[i] + ","
  strLine = strLine + "%.2f" % AgMu[i] + ","
  strLine = strLine + "%.2f" % AgSe[i] + ","
  strLine = strLine + "%s"   % spNa[i] + "\n"
  f.write(strLine)  
f.close()


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
