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

import edu.stanford.ejalbert.BrowserLauncher as bl


App = dt2.DTSA2.getInstance()
MainFrame = App.getFrame()
Database = dt2.DTSA2.getSession()
DefaultOutput = (globals()["DefaultOutput"] if globals().has_key("DefaultOutput") else None)
DataManager = dt2.DataManager.getInstance()
StdOut = MainFrame.getStandardOutput()
StdErr = MainFrame.getStandardError()
terminated = False

# remove all the selected spectra
sel = DataManager.getInstance().getSelected()
l = len(sel)
for  i in  range(l):
   print i
   DataManager.removeSpectrum(sel[i])

# a = DataManager.getInstance().getSelected()[0]

# print a

# print type(a)

# DataManager.removeSpectrum(a)





