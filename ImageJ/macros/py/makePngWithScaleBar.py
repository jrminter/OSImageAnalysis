# makePngWithScaleBar.py
#
# J. R. Minter
#
# Selects the current image file. Assumes the image is calibrated.
# Changes the image to RGB. Burn a scale bar. Outputs a .png file
# to the specified path.
#
# CCA license
#   date.     who. comment
# ----------  ---  -----------------------------------------------------
# 2019-05-04  JRM  initial prototype.
#
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver
import jmFijiGen as jmg

tic = time.time()
sleepTime = 3         # pause to see ong in sec
scaleX = 0.03143555   # um/px X
scaleY = 0.03144531   # um/px y
barW = 1.0            # bar width, microns
barH = 6              # bar height, pts
barF = 24             # bar font, pts
barC = "Black"        # bar color
barL = "Lower Right"  # bar location

homDir = os.environ['HOME']
relDir = "/Dropbox/datasets/AgX-dat/eia2855ImgSeries"
imgNam = "IMAGE027.tif"

imgPath = homDir + relDir + "/" + imgNam

IJ.open(imgPath);
IJ.run("Properties...", "channels=1 slices=1 frames=1 unit=um pixel_width=0.03143555 pixel_height=0.03144531 voxel_depth=1.0000000");
orig = IJ.getImage();

ti = orig.getShortTitle();
pngPath = homDir + relDir + "/" + ti + ".png"

strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
# a hack to get the scale bars to work reliably
IJ.run(orig, "RGB Color", "")

# dummy to get things set
foo = orig.duplicate()
IJ.run(foo, "Add Scale Bar", strBar)
# explicitly save preferences
Prefs.savePreferences()
foo.changes = False
foo.close()

IJ.run(orig, "Add Scale Bar", strBar)
print(pngPath)

fs = FileSaver(orig)
if fs.saveAsPng(pngPath):
	print "png saved successfully at ", pngPath  

time.sleep(sleepTime)

orig.close()
