# AnaBX61IJ_.py
#
# Image-J Jython macro to process a series of TIF images recorded from
# the IAM-1 stage micrometer on the Olympus BX-61 with with a
# 50X/0.85 NA objective and a 2X transfer lens w/ 2X interpolation. 
# Requires the Analyze_Line plugin.
#
# J. R. Minter
#
#    Date      By   Comments
# 2013-05-21  JRM  Initial prototype. Requires Analyse_Line.class 
#                  v. 0.1.500


from ij import IJ
import ij.util.Tools
from java.awt import Color
import os
import sys

def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)


strImgRoot = os.environ['IMG_ROOT']
# relative path to images
strRel="/std/line/qm-03859-IAM1-BX61-tif/"
strRptPath = strImgRoot + "/std/line/rpt/qm-03859-IAM1-BX61-50-tif/"
strPngPath = strRptPath + "png/"
ensure_dir(strRptPath)
ensure_dir(strPngPath)

strPath = strImgRoot + strRel
umPerPx = 0.0369566
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
  strCmd = "min=200 max=999999 top/bottom=5 lo=0.25 med=0.50 hi=0.75 log=0 path="
  strCmd += strRptPath + " report=" + strRpt
  IJ.run("Analyze Line", strCmd)
  IJ.selectWindow(imp.getTitle())
  strImgOut =  strPngPath + Tools.split(imp.getTitle(), ".")[0] + ".png"
  IJ.saveAs("PNG", strImgOut)
  IJ.run("Close")


