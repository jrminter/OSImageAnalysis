from ij import IJ
import ij.util.Tools
from java.awt import Color
import os

strHome = os.environ['HOME']
strProjDir = "/work/proj/analyzeLineIJ/"
umPerPx = 0.036861

# should not need to change below here...
strImage = strHome + strProjDir + "tif/line.tif"
strUmPerPx = str(umPerPx)
strRptPath = strHome + strProjDir + "csv/"

strCal = "channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal += strUmPerPx
strCal += " pixel_height="
strCal += strUmPerPx
strCal += "  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"

imp = IJ.openImage(strImage)
IJ.run(imp, "Properties...", strCal)
imp.show()

strRpt = Tools.split(imp.getTitle(), ".")[0] + ".csv"
strCmd = "min=10 max=999999 top/bottom=5 lo=0.25 med=0.50 hi=0.75 log=0 path="
strCmd += strRptPath + " report=" + strRpt

IJ.run("Analyze Line", strCmd)


