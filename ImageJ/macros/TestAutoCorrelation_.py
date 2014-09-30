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
from ij import IJ
from ij import ImagePlus
from ij.plugin.filter import Analyzer
from ij.process import ImageStatistics as IS
from ij.process import FloatProcessor
from ij.measure import Measurements as IM
import ij.WindowManager as WM
import os

bVerbose = True
bMakeBinary = True

# N.B. this expects an environment variable with the path
# to images in the git repository.
gitHome = os.environ['GIT_HOME']

# note the expected folder structure
strPath = gitHome + "/OSImageAnalysis/images/"
strName="cross-grating"
strExt=".tif"

halfWidth = 64 # how far out we crop the autocorrelation

strFile=strPath+strName+strExt
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
  IJ.run("Set Measurements...", "area centroid redirect=None decimal=3");
  IJ.run("Analyze Particles...", "display exclude clear include");




