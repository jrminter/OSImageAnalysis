# listDetCals.py
import sys
import shutil
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3,FluorescenceXRayGeneration3, XRayTransport3", None)


import os
import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQTools as ept
import gov.nist.microanalysis.Utility as epu
# This next two lines of weirdness eliminate a "no module named" error.  Why????
import sys as sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte", "MonteCarloSS", None)
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.dtsa2 as dt2
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import java.lang as jl
import java.io as jio
import java.util as ju
import jarray
import javax.imageio as ii

def listDetCalibrations(det):
    """listDetCalibrations(det, outPath)
    Tabulate the calibrations for the specified detector to the specified output file
    Example:
        det = findDetector("FEI CM20UT EDAX-RTEM")
        tabulateDetCalibrations(det)
    (Contributed by John Minter)"""
    Database = dt2.DTSA2.getSession()
    print(det.getName())
    dp = det.getDetectorProperties()
    cals = Database.getCalibrations(dp)
    iCnt = 0
    lDa = []
    lCw = []
    lZo = []
    lRe = []
    print(len(cals))
    for cal in cals:
        ad = cal.getActiveDate()
        lDa.append(ad.toString())
        cw = cal.getChannelWidth()
        lCw.append(cw)
        zo = cal.getZeroOffset()
        lZo.append(zo)
        cp = cal.getProperties()
        res = cp.getNumericProperty(cp.Resolution)
        lRe.append(res)
        lin = cp.getTextProperty(cp.ResolutionLine)
        iCnt = iCnt + 1
    # write out results
    strLine = 'active.date, channel.width.eV, zero.offset.eV, resolution.eV'
    print(strLine)
    for i in range(iCnt):
        strLine = "%s" % lDa[i] + ","
        strLine = strLine + "%.5f" % lCw[i] + ","
        strLine = strLine + "%.5f" % lZo[i] + ","
        strLine = strLine + "%.2f" % lRe[i] # + "\n"
        print(strLine)

gitDir  = os.environ['GIT_HOME']
prjDir  = "/OSImageAnalysis/dtsa2/productionScripts/"
relPy   = "listDetCalibrations Results/"
rptDir  = gitDir + prjDir + relPy

# det = findDetector("Oxford p4 05eV 2K")
det = findDetector("Oxford p4 05eV 4K")
# det = findDetector("FEI FIB620 EDAX-RTEM")

listDetCalibrations(det)



# clean up cruft
shutil.rmtree(rptDir)
print "Done!"

