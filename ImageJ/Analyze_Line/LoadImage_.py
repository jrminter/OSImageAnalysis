from ij import IJ
from java.awt import Color

# strBasePath="C:\\Data\\atd\\images\\"
strBasePath="D:\\Data\\images\\"
strFile="std\\line\\line.tif"
umPerPx="0.036861"

strImage=strBasePath + strFile
strCal="channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal+=umPerPx
strCal+=" pixel_height="
strCal+=umPerPx
strCal+="  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"
   
imp = IJ.openImage(strImage)
IJ.run(imp, "Properties...", strCal)
imp.show()
rt = ResultsTable()
print dir(rt)