from ij import IJ
from java.awt import Color

strBasePath="C:\\Data\\atd\\images\\"
# strBasePath="D:\\Data\\images\\"
strFile="std\\line\\line.tif"
strRepBase="std\\line\\"
strRept="line.csv"
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

strCmd1="min=10 max=999999 top/bottom=5 lo=0.25 med=0.50 hi=0.75 log=0 path="
strReptPath=strBasePath+strRepBase
strCmd2=" report="

strCmd=strCmd1 + strReptPath + strCmd2 + strRept

# print(strCmd)
IJ.run("Analyze Line", strCmd)

