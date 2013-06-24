# getTransitionEnergy.py

def getKalphaEnergy(elmName):
  """getKalphaEnergy("Cu")
  Returns the transion energy (in keV) for the element's K-alpha line as the weighted sum of Ka1 and Ka2"""
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
  Returns the transion energy (in keV) for the element's L-alpha line as the weighted sum of La1 and La2"""
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
  returns the weighted energy (in keV) for the element's K-alpha and L-alpha lines"""
  enK = getKalphaEnergy(elmName)
  enL = getLalphaEnergy(elmName)
  res = "%s - K-alpha = %.4f, L-alpha = %.4f" % (elmName, enK, enL)
  return res
  
  

en = getKLenergy('Cu')
print (en)

en = getKLenergy('Mo')
print (en)

en = getKLenergy('Ni')
print (en)

el='Al'
en = getKalphaEnergy(el)
res = "%s - K-alpha = %.4f" % (el, en)
print (res)

el='C'
en = getKalphaEnergy(el)
res = "%s - K-alpha = %.4f" % (el, en)
print (res)

el='O'
en = getKalphaEnergy(el)
res = "%s - K-alpha = %.4f" % (el, en)
print (res)

el='F'
en = getKalphaEnergy(el)
res = "%s - K-alpha = %.4f" % (el, en)
print (res)

