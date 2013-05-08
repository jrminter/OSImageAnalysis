from ij import IJ
from java.awt import Color

strBasePath="C:\\Data\\atd\\images\\"
# strBasePath="D:\\Data\\images\\"
strFile="std\\line\\line.tif"
umPerPx="0.036861"

strImage=strBasePath + strFile
strCal="channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal+=umPerPx
strCal+=" pixel_height="
strCal+=umPerPx
strCal+="  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"
   
imp = IJ.openImage(strImage)
imp2 = imp.duplicate()
imp3 = imp.duplicate()
IJ.run(imp, "Properties...", strCal)
# ip=imp.getProcessor()
IJ.setAutoThreshold(imp, "Default dark")
imp.show()
table = ResultsTable()
# Create a hidden ROI manager, to store a ROI for each blob or cell
roim = RoiManager(False)
# measurements = Measurements.MEAN + Measurements.CENTROID
pa = ParticleAnalyzer(ParticleAnalyzer.ADD_TO_MANAGER, Measurements.AREA, table, 5, Double.POSITIVE_INFINITY, 0.0, 1.0)

# IJ.run(imp, "Set Measurements...", "  mean center bounding redirect=None decimal=3" )
# IJ.run(imp, "Analyze Particles...", "size=5-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear" )

if pa.analyze(imp):
  print "All ok"
else:
  print "There was a problem in analyzing"
 
# The measured areas are listed in the first column of the results table, as a float array:
res = table.getColumn(0)
print table

# Create a new list to store the mean intensity values of each blob:
means = []
 
for roi in RoiManager.getInstance().getRoisAsArray():
  imp.setRoi(roi)
  stats = imp.getStatistics(Measurements.MEAN)
  means.append(stats.mean)

grayBkg = 0.5*(means[0]+means[1])

print grayBkg

manager = RoiManager.getInstance()
manager.runCommand("Deselect")
n=manager.getCount()
for i in xrange(0,n):
   l=n-i-1
   manager.select(l)
   manager.runCommand("Delete")
imp.show()

IJ.setAutoThreshold(imp2, "Default")
# Create a table to store the results
table = ResultsTable()
# Create a hidden ROI manager, to store a ROI for each blob or cell
roim = RoiManager(False)
# measurements = Measurements.MEAN + Measurements.CENTROID
pa = ParticleAnalyzer(ParticleAnalyzer.ADD_TO_MANAGER, Measurements.AREA, table, 5, Double.POSITIVE_INFINITY, 0.0, 1.0)

# IJ.run(imp, "Set Measurements...", "  mean center bounding redirect=None decimal=3" )
# IJ.run(imp, "Analyze Particles...", "size=5-Infinity circularity=0.00-1.00 show=[Overlay Outlines] display clear" )

if pa.analyze(imp2):
  print "All ok"
else:
  print "There was a problem in analyzing"
 
# The measured areas are listed in the first column of the results table, as a float array:
res = table.getColumn(0)

# Create a new list to store the mean intensity values of each blob:
means = []
 
for roi in RoiManager.getInstance().getRoisAsArray():
  imp2.setRoi(roi)
  stats = imp2.getStatistics(Measurements.MEAN)
  means.append(stats.mean)

grayLin=means[0]
print grayLin

thrGray = 0.5*(grayLin+grayBkg)

manager = RoiManager.getInstance()
manager.runCommand("Deselect")
n=manager.getCount()
for i in xrange(0,n):
   l=n-i-1
   manager.select(l)
   manager.runCommand("Delete")
 
# print(dir(ip))
imp2.show()
imp.close()
imp.flush()

ip3 = imp3.getProcessor()

# 2 - Apply a threshold: only zeros and ones
# Set the desired threshold range: keep from 0 to 74
ip3.setThreshold(0, thrGray,  ImageProcessor.NO_LUT_UPDATE)
imp3.setProcessor("work", ip3)
imp3.show()
imp2.close()
imp2.flush()

tableCOM = ResultsTable()
# Create a hidden ROI manager, to store a ROI for each blob or cell
roim = RoiManager(False)

pa = ParticleAnalyzer(ParticleAnalyzer.ADD_TO_MANAGER, Measurements.AREA, tableCOM, 5, Double.POSITIVE_INFINITY, 0.0, 1.0)
if pa.analyze(imp3, ip3):
  print "All ok"
else:
  print "There was a problem in analyzing imp3"
 
# The measured areas are listed in the first column of the results table, as a float array:
centsX = tableCOM.getColumn(0)
for cX in centsX:  print cX

for roi in RoiManager.getInstance().getRoisAsArray():
  imp3.setRoi(roi)
  IJ.run("Measure")
  rect=roi.getBoundingRect()
  x0 = rect.x + 0.5*rect.width
  y0 = rect.y + 0.5*rect.height
  print x0,y0

# some useful info here:
# http://imagej.1557.x6.nabble.com/alternative-to-doWand-x-y-td3702625.html

IJ.doWand(int(x0), int(y0))
theROI = imp3.getRoi()
nPts=theROI.getConvexHull().npoints
print nPts

iX=theROI.getConvexHull().xpoints
iY=theROI.getConvexHull().ypoints

fX = []
fY = []

for i in xrange(0,nPts-1):
   fX.append(float(iX[i]))
   fY.append(float(iY[i]))

polyHull = FloatPolygon(fX, fY, nPts)
hullRoi = PolygonRoi(polyHull, Roi.POLYGON)

