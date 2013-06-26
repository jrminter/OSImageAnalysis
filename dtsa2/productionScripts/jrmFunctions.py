# jrmFunctions.py
# John Minter's DTSA-II Jython Script Functions
# Licenced under the GPL2 | BSD License
# Version 0.9.0  2013-06-26
#

import os
import sys
import shutil

# Define functions
def clearAllSpectra():
  """clearAllSpectra()
  Clear all spectra from the data manager. Loaded from jrmFunctions.py."""
  DataManager = dt2.DataManager.getInstance()
  DataManager.clearSpectrumList()

def compPeakIntegral(spect, kev, widEv, digits=1):
  """compPeakIntegral( spect, kev, widEv, digits=1)
  Compute the background-corrected peak interval for the line at kev keV with an
  integration width of widEv eV and return the results the desired (typically 1)
  following the decimal. Loaded from jrmFunctions.py."""
  ev = 1000*kev
  hw = 0.5*widEv
  start = ev - hw
  end = ev + hw
  res = epq.SpectrumUtils.backgroundCorrectedIntegral(spect, start, end)
  r0 = round(res[0],digits)
  r1 = round(res[1],digits)
  # note: under the hood, this returns the estimate, res[0] 
  # and the uncertainty, res[1]. Typically it is one digit.
  # r0  = '%.0f' % res[0]
  # r1  = '%.0f' % res[1]
  ret = [r0, r1]
  return ret


def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it.
  Loaded from jrmFunctions.py."""
  if not os.path.exists(d):
    os.makedirs(d)

def getKalphaEnergy(elmName):
  """getKalphaEnergy("Cu")
  Returns the transion energy (in keV) for the element's K-alpha
  line as the weighted sum of Ka1 and Ka2. Loaded from jrmFunctions.py."""
  elm = element(elmName)
  xrt = epq.XRayTransition.KA1
  try:
    if epq.XRayTransition.exists(elm, xrt):
      tr = epq.XRayTransition(elm, xrt)
      en1 = epq.FromSI.keV(tr.getEnergy())
      wt1 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      xrt = epq.XRayTransition.KA2
      tr = epq.XRayTransition(elm, xrt)
      en2 = epq.FromSI.keV(tr.getEnergy())
      wt2 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      en = (wt1*en1+wt2*en2)/(wt1+wt2)
      return round(en, 4) 
    else:
      print "invalid element"
      return -1.0
  except jl.IllegalArgumentException:
    pass

def getLalphaEnergy(elmName):
  """getLalphaEnergy("Cu")
  Returns the transion energy (in keV) for the element's L-alpha line as
  the weighted sum of La1 and La2. Loaded from jrmFunctions.py."""
  elm = element(elmName)
  xrt = epq.XRayTransition.LA1
  try:
    if epq.XRayTransition.exists(elm, xrt):
      tr = epq.XRayTransition(elm, xrt)
      en1 = epq.FromSI.keV(tr.getEnergy())
      wt1 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      xrt = epq.XRayTransition.LA2
      tr = epq.XRayTransition(elm, xrt)
      en2 = epq.FromSI.keV(tr.getEnergy())
      wt2 = tr.getWeight(epq.XRayTransition.NormalizeKLM)
      en = (wt1*en1+wt2*en2)/(wt1+wt2)
      return round(en, 4) 
    else:
      print "invalid element"
      return -1.0
  except jl.IllegalArgumentException:
    pass

def getKLenergy(elmName):
  """getKLenergy(elmName)
  returns the weighted energy (in keV) for the element's K-alpha and
  L-alpha lines as a dictonary. Loaded from jrmFunctions.py."""
  enK = getKalphaEnergy(elmName)
  enL = getLalphaEnergy(elmName)
  res = {"K-alpha" : enK, "L-alpha" : enL}
  return res

def spcTopHatFilter(spc, det, e0, fw=150, norm=False):
  """spcTopHatFilter(spc, det, e0, fw=150, norm=False):
  Compute a top hat filter for spectrum spc with the given detector
  the specified kV (e0) with the desired filter width and normalization.
  Loaded from jrmFunctions.py.
  """
  rawName=spc.getProperties().getTextProperty(epq.SpectrumProperties.SpectrumDisplayName)
  fltName=rawName+"-thf"
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin, 1.0)
  spc.getProperties().setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  sw=wrap(spc)
  spc=sw
  thf=epq.FittingFilter.TopHatFilter(fw, det.getChannelWidth())
  fs=epq.FilteredSpectrum(spc, norm)
  fs.setFilter(thf)
  fs.getProperties().setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, fltName)
  fsw=wrap(fs)
  return fsw


