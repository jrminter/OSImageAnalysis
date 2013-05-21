from ij import IJ
import ij.util.Tools
from java.awt import Color
import os
import sys


strImgRoot = os.environ['IMG_ROOT']
# relative path to images
strRel="/std/line/qm-03860-IAM1-BX60-tif/"
strRptPath = strImgRoot + "/std/line/rpt/qm-03860-IAM1-BX60-tif/"
strPath = strImgRoot + strRel
umPerPx = 0.0368365
strUmPerPx = str(umPerPx)

strCal = "channels=1 slices=1 frames=1 unit=micron pixel_width="
strCal += strUmPerPx
strCal += " pixel_height="
strCal += strUmPerPx
strCal += "  voxel_depth=1.0000000 frame=[0 sec] origin=0,0"

# print strPath

for file in os.listdir(strPath):
  print file
  sFile = os.path.join(strPath, file)
  imp = IJ.openImage(sFile)
  imp.show()
  IJ.run(imp, "Properties...", strCal)
  IJ.run("16-bit")
  imp.show()
  strRpt = Tools.split(imp.getTitle(), ".")[0] + "-ij.csv"
  strCmd = "min=10 max=999999 top/bottom=5 lo=0.25 med=0.50 hi=0.75 log=0 path="
  strCmd += strRptPath + " report=" + strRpt
  IJ.run("Analyze Line", strCmd)
  
