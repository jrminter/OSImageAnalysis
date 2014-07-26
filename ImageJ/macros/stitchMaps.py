# -*- coding: utf-8 -*-
# stitchMaps.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-07-26  JRM 0.1.00  initial prototype development
import os
import glob
import time

fMag = 2.0
sPath = "D:\\Data\\images\\test\\map\\"
query = sPath + "*.png"
lFiles = glob.glob(query)
lW = []
lH = []
for fi in lFiles:
  imp = ImagePlus(fi)
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
  imp = ImagePlus(fi)
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
  else:
    strName = os.path.basename(fi).strip(".png")
    strCmd = "x=%.3lf y=%.3lf interpolation=Bicubic create title=%s" % (fMag, fMag, strName)
    IJ.run("Scale...", strCmd)
    # IJ.run("Close")
    imp.close()
    hBig = float(ip.height)*fMag
    wBig = float(ip.width)*fMag


print(int(hMain), int(hBig))
delta = hBig-hMain + 1
IJ.makeRectangle(0, 0, wBig, hBig - delta )
IJ.run("Crop")
# to-do: crop the line
# print(lW)
# print(lH)