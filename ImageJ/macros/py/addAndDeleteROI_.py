# addAndDeleteROI_.py
# Add and delete a ROI from an image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-21  JRM 0.1.00  Initial prototype

from ij import WindowManager
from ij import IJ
from ij.plugin.frame import RoiManager

raw = IJ.openImage("D:\\Data\\images\\tmp\\sis-efi-sc.png")
raw.show()
IJ.makeRectangle(0, 190, 1600, 260)
wbROI = raw.getRoi()
if (wbROI==None):
  exit("you must draw region first")
print(wbROI)
rm = RoiManager()
rm.select(raw, 0)
rm.runCommand("Show All")
rm.runCommand("Draw")
