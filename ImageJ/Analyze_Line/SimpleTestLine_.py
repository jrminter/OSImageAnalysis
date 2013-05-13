from ij import IJ
from java.awt import Color

strBasePath="C:\\Data\\atd\\images\\"
# strBasePath="D:\\Data\\images\\"
strFile="std\\line\\line.tif"
umPerPx="0.036861"
fCal = 0.036861

strImage=strBasePath + strFile
strCal="channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal+=umPerPx
strCal+=" pixel_height="
strCal+=umPerPx
strCal+="  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"
   
imp = IJ.openImage(strImage)
IJ.run(imp, "Properties...", strCal)

# just detect the line
IJ.setAutoThreshold(imp, "Default")
imp.show()
tableCOM = ResultsTable()
# Create a hidden ROI manager, to store a ROI for each blob or cell
roim = RoiManager(True)
pa = ParticleAnalyzer(ParticleAnalyzer.ADD_TO_MANAGER, Measurements.AREA+Measurements.CENTROID, tableCOM, 5, Double.POSITIVE_INFINITY, 0.0, 1.0)
ip = imp.getProcessor()
if pa.analyze(imp, ip):
  print "All ok"
else:
  print "There was a problem in analyzing imp"
 
# The measured areas are listed in the first column of the results table, as a float array:

iX = (int) (tableCOM.getValue("X", 0)/fCal);
iY = (int) (tableCOM.getValue("Y", 0)/fCal);

theROI=roim.getInstance().getRoisAsArray()[0]
linePoly = theROI.getInterpolatedPolygon(1.0, False)
lineRoi = PolygonRoi(linePoly.duplicate(), Roi.POLYGON)
polyFloat = lineRoi.getFloatPolygon()
# print dir(polyFloat)
xh = []
yh = []
nPts=polyFloat.npoints
xh=polyFloat.xpoints
yh=polyFloat.ypoints
imp.setTitle("ana-"+imp.getTitle())
print nPts
tableCOM = ResultsTable()
for i in xrange(0,nPts-1):
   tableCOM.setValue("X", i, xh[i])
   tableCOM.setValue("Y", i, yh[i])

tableCOM.show("coords")



roim.dispose()





