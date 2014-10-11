# TestAutoCorrelation_.py
#
# Process a cross-grating image to generate and analyze an autocorreation
# to get the calibration
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-29  JRM 0.1.00  Initial prototype
#

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from math import sqrt
from ij import IJ
from ij import ImagePlus
from ij.plugin.filter import Analyzer
from ij.process import ImageStatistics as IS
from ij.process import FloatProcessor
from ij.measure import Measurements as IM
from ij.measure import ResultsTable
import ij.WindowManager as WM
import os

bVerbose = False
bMakeBinary = True
iDigits = 4

# N.B. this expects an environment variable with the path
# to images in the git repository.
gitHome = os.environ['GIT_HOME']

# note the expected folder structure
strPath = gitHome + "/OSImageAnalysis/images/"
strName="cross-grating"
strExt=".tif"

halfWidth = 64 # how far out we crop the autocorrelation
space = 1000.0/2160. # microns
print("space = %.4f microns" % space)

# a = [0xCE, 0xBC]
# mu = "".join([chr(c) for c in a]).decode('UTF-8')
# units  = mu+"m/px"
units = "microns/px"
iUnits = "px/micron"

strFile=strPath+strName+strExt
strRpt=strPath+strName+".csv"
strMath="image1=" + strName + " operation=Correlate image2=" + strName + " result=Result do"
# print(strFile)
imp = IJ.openImage(strFile)
imp.setTitle(strName)
imp.show()
IJ.run("32-bit");
IJ.run("FD Math...", strMath)
IJ.selectWindow(strName)
IJ.run("Close")

IJ.selectWindow("Result")
imp=WM.getCurrentImage()
ip = imp.getProcessor()
options = IM.MEAN | IM.MEDIAN | IM.MIN_MAX | IM.STD_DEV
stats = IS.getStatistics(ip, options, imp.getCalibration())
if bVerbose:
  print "   Min:", IJ.d2s(stats.min,2)
  print "   Man:", IJ.d2s(stats.max,2)
  print "   Mean:", IJ.d2s(stats.mean,2)
  print "Std Dev:" , IJ.d2s(stats.stdDev,2)

delta = stats.max - stats.min
pixels = ip.getPixels()
newPixels = map(lambda x: (x - stats.min)/delta, pixels)
ipSub = FloatProcessor(ip.width, ip.height, newPixels, None)
impSub = ImagePlus("Sub", ipSub)
impSub.show()
IJ.selectWindow("Result")
IJ.run("Close")
IJ.selectWindow("Sub")
imp=WM.getCurrentImage()
imp.setTitle(strName+"-acf")
imp.show()

centX = ip.width/2
centY = ip.height/2
top = centX-halfWidth
left = centY-halfWidth
IJ.makeRectangle(top,left,2*halfWidth,2*halfWidth)
IJ.run("Crop")
IJ.setThreshold(0.65, 1.00)
Analyzer.setOption("BlackBackground", False)
if bMakeBinary:
  IJ.run("Make Binary")
  IJ.run("Convert to Mask")
  IJ.run("Set Measurements...", "area centroid redirect=None decimal=3")
  IJ.run("Analyze Particles...", "display exclude clear include")
  rt = ResultsTable.getResultsTable()
  nMeas = rt.getCounter()
  print(nMeas)
  cntX  = rt.getColumn(ResultsTable.X_CENTROID)
  cntY  = rt.getColumn(ResultsTable.Y_CENTROID)
  cntA  = rt.getColumn(ResultsTable.AREA)
  # find the center - will be closest to half width
  fHw = float(halfWidth)
  minDelta = 1000000.
  X0 = 0.
  Y0 = 0.
  iMin = 0
  
  for i in range(len(cntX)):
    dX = cntX[i] - fHw
    dY = cntY[i] - fHw
    delta = sqrt(dX*dX+dY*dY)
    if (delta < minDelta):
      minDelta = delta
      X0 = cntX[i]
      Y0 = cntY[i]
      iMin = i

  for i in range(len(cntX)):
    cntX[i] -= X0
    cntY[i] -= Y0

  # write output file
  f=open(strRpt, 'w')
  strLine = 'X0,Y0,Area\n'
  f.write(strLine)
  for i in range(len(cntX)):
    strLine = "%.4f, %.4f, %.4f\n" % (cntX[i], cntY[i], cntA[i] )
    f.write(strLine)
  f.close()
  
  dX = cntX[iMin-1] 
  dY = cntY[iMin-1]
  R1 = round(space/sqrt(dX*dX+dY*dY), iDigits+2)
  iR1 = round(sqrt(dX*dX+dY*dY)/space, iDigits)
  dX = cntX[iMin+1] 
  dY = cntY[iMin+1]
  R2 = round(space/sqrt(dX*dX+dY*dY), iDigits+2)
  iR2 = round(sqrt(dX*dX+dY*dY)/space, iDigits)
    
  
  print(R1, R2, units)
  print(iR1, iR2, iUnits)




