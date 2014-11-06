from ij import IJ
import jmFijiGen as jmg
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable

def whiteBalance(imp, lROI, bVerbose=False):
  """whiteBalance(imp, lROI, bVerbose=False)
  White balance an image from a ROI. Requires a ROI of the neutral area.
  Adapted from the macro by  Vytas Bindokas; Oct 2006, Univ. of Chicago
  Input parameters
  imp - the input ImagePlus
  bVerbose - a boolean, default False, whether to print info
  Returns
  An ImagePlus of the corrected image (displayed)"""
  if(imp==None):
    IJ.error("Missing Image","you must have an image with a region first")
    return None
  name = imp.getShortTitle()
  w = imp.getWidth()
  h = imp.getHeight()

  ret = imp.duplicate() 
  ret.setRoi(lROI[0], lROI[1], lROI[2], lROI[3]) 
  IJ.run(ret, "RGB Stack", "")
  ret.setRoi(lROI[0], lROI[1], lROI[2], lROI[3]) 
  rm = RoiManager()
  rm.select(0)
  ret.setSlice(1)
  IJ.run(ret, "Measure","")
  ret.setSlice(2)
  IJ.run(ret, "Measure","")
  ret.setSlice(3)
  IJ.run(ret, "Measure","")
  rt = ResultsTable.getResultsTable()
  mc = rt.getColumnIndex("Mean")
  ct = rt.getCounter()
  r = rt.getValueAsDouble(mc, 0)
  g = rt.getValueAsDouble(mc, 1)
  b = rt.getValueAsDouble(mc, 2)
  t=((r+g+b)/3)
  dR=r-t
  dG=g-t
  dB=b-t
  # val = rt.getValueAsDouble(0, 0)
  if(bVerbose==True):
    print(name)
    print("ROI:")
    print(wbROI)
    print("Mean R,G,B")
    print(r,g,b)
    print("Mean dR,dG,dB")
    print(dR,dG,dB)
  # R=getResult("Mean")
  ret.setRoi(0, 0, w, h)
  IJ.run(ret,"16-bit","")
  IJ.run(ret,"32-bit","")
  ret.setSlice(1)
  strSlice = "slice value=%f" % abs(dR)
  if (dR<0):
    IJ.run(ret, "Add...", strSlice )
  if (dR>0):
    IJ.run(ret, "Subtract...", strSlice)
  
  ret.setSlice(2)
  strSlice = "slice value=%f" % abs(dG)
  if (dG<0):
    IJ.run(ret, "Add...",  strSlice )
  if (dG>0):
    IJ.run(ret, "Subtract...",  strSlice )

  strSlice = "slice value=%f" % abs(dB)
  ret.setSlice(3)
  if (dB<0):
    IJ.run(ret, "Add...", strSlice )
  if (dB>0):
    IJ.run(ret, "Subtract...", strSlice )
    
  rm.runCommand("Deselect")
  IJ.run(ret, "16-bit", "")
  IJ.run(ret, "Convert Stack to RGB","")
  IJ.run(ret, "RGB Color", "slices");
  # ret.setTitle(name + "-wb")

  return ret


# print(dir(IJ))
imp = IJ.getImage()
lROI = [127, 155, 227, 164]
ret = whiteBalance(imp, lROI, bVerbose=False)
ret.show()
