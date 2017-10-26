from ij import IJ
from ij import ImagePlus

factor = 0.85
imp = IJ.getImage()
ip = imp.getProcessor()
maxGray = ip.getMax()
print(maxGray)
hist = ip.getHistogram()
# print(hist)
maxV = ip.getHistogramMax()
print(len(hist))
print(maxV)

