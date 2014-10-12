from ij import IJ
import ij.util.Tools
from java.awt import Color
import os
import sys


strImgRoot = os.environ['IMG_ROOT']
# relative path to images
strRel="/std/Cr-line/qm-03860-IAM1-BX60-tif/"
strPath = strImgRoot + strRel
umPerPx = 0.0368365

a = [0xC2, 0xB5]
mu = "".join([chr(c) for c in a]).decode('UTF-8')
# mu = IJ.fromCharCode(181)
micron = mu + "m"

strCal = "channels=1 slices=1 frames=1 unit=%s pixel_width=" % micron
strCal += str(umPerPx)
strCal += " pixel_height="
strCal += str(umPerPx)
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
  imp.close()
  
