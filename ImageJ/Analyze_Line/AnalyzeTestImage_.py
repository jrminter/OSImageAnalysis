from ij import IJ
import ij.util.Tools
from java.awt import Color
import os

strGitHome = os.environ['GIT_HOME']
strImgDir = "/OSImageAnalysis/ImageJ/Analyze_Line/std/"
umPerPx = 0.0368365

# should not need to change below here...
strImage = strGitHome + strImgDir + "line.tif"
strUmPerPx = str(umPerPx)
strRptPath = strGitHome + strImgDir

strCal = "channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal += strUmPerPx
strCal += " pixel_height="
strCal += strUmPerPx
strCal += "  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"

imp = IJ.openImage(strImage)
IJ.run(imp, "Properties...", strCal)
imp.show()
IJ.run("16-bit")
imp.show()

strRpt = Tools.split(imp.getTitle(), ".")[0] + "-ij.csv"
strCmd = "min=200 max=999999 top/bottom=5 lo=0.25 med=0.50 hi=0.75 log=0 path="
strCmd += strRptPath + " report=" + strRpt

IJ.run("Analyze Line", strCmd)


