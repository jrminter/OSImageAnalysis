import os
import glob
import time
from ij import IJ as IJ

dOrigScale = 57.9/256.0
sUnit = "um"
edsDir = os.environ['EDS_ROOT']
relDir = "/Oxford/QM14-04-02H-Armstrong/reports/maps/S1-uhr-7kV-map-02/"
# opening this got it right so I could set type to RGB...
# convert 4-line.png -set colorspace RGB 4-lineRGB.png

fMag = 2.0
sPath = edsDir + relDir
sPath = sPath.replace("/","\\")
print(sPath)
query = sPath + "*.png"
lFiles = glob.glob(query)
lW = []
lH = []
for fi in lFiles:
  imp = IJ.openImage(fi)
  imp.show()
  ip = imp.getProcessor()
  lW.append(ip.width)
  lH.append(ip.height)
  # time.sleep(1)
  IJ.run("Close")

minW = float(min(lW))
maxW = float(max(lW))
scFa = maxW/minW
print(scFa)

hMain = 0
hBig = 0

for fi in lFiles:
  imp = IJ.openImage(fi)
  imp.show()
  ip = imp.getProcessor()
  if (ip.width < maxW):
    # time.sleep(1)
    strName = os.path.basename(fi).strip(".png")
    strCmd = "x=%.3lf y=%.3lf interpolation=Bicubic create title=%s" % (fMag*scFa, fMag*scFa, strName)
    IJ.run("Scale...", strCmd)
    # IJ.run("Close")
    imp.close()
    hMain = float(ip.height)*fMag*scFa
    strScale = "distance=1 known=%.3f pixel=1 unit=%s global" % (dOrigScale*fMag*scFa, sUnit)
    IJ.run("Set Scale...", strScale)
  else:
    strName = os.path.basename(fi).strip(".png")
    strCmd = "x=%.3lf y=%.3lf interpolation=Bicubic create title=%s" % (fMag, fMag, strName)
    IJ.run("Scale...", strCmd)
    # IJ.run("Close")
    imp.close()
    strScale = "distance=1 known=%.3f pixel=1 unit=%s global" % (dOrigScale*fMag, sUnit)
    IJ.run("Set Scale...", strScale)
    hBig = float(ip.height)*fMag
    wBig = float(ip.width)*fMag


print(int(hMain), int(hBig))
delta = hBig-hMain + 1
IJ.makeRectangle(0, 0, wBig, hBig - delta )
IJ.run("Crop")
# to-do: crop the line
# print(lW)
# print(lH)