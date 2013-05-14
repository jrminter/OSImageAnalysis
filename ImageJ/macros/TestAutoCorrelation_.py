from ij import IJ
from ij.process import ImageStatistics as IS
import ij.WindowManager as WM

strPath="D:/Data/images/cross-grating-img/"
strName="cross-grating"
strExt=".dm3"

halfWidth = 256 # how far out we crop the autocorrelation

strFile=strPath+strName+strExt
strMath="image1=" + strName + " operation=Correlate image2=" + strName + " result=Result do"

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
options = IS.MEAN | IS.MEDIAN | IS.MIN_MAX | IS.STD_DEV
stats = IS.getStatistics(ip, options, imp.getCalibration())

# print "   Min:", IJ.d2s(stats.min,2)
# print "   Man:", IJ.d2s(stats.max,2)
# print "   Mean:", IJ.d2s(stats.mean,2)
# print "Std Dev:" , IJ.d2s(stats.stdDev,2)

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


