# stitchOxfordEdsMaps_.py
#
# Stitch Oxford EDS maps and burn scale bars
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-11  JRM 0.1.00  initial prototype development.
# 2014-09-15  JRM 0.1.10  added cropping and saving output

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager

edsDir  = os.environ['EDS_ROOT']
rptDir  = os.environ['RPT_ROOT']
# for uncropped images
# relImg  = "/testMap/png/ij"
# for cropped images
relImg  = "/testMap/tile"
relOut  = "/testMap/out"
outNam = "445005-248-Pd8-1-FIB-7kV-m01-3x2.png"

imgDir = edsDir + relImg

print(imgDir)

# 2X3
# x      = 2
# y      = 3
# 3X2
x      = 3
y      = 2
scale  = 2.822
units  = "nm"
pts    = 32
barCol = "Black"

def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)

def stitchMaps(tifDir, cols, rows, scaFac, scaUni, barWid, barHt, barFnt, barCol, barLoc ):
  """stitchMaps(tifDir, cols, rows)
  stitch images from an Oxford Map
  parameters:
  tifDir - directory with tif files
  cols   - number of columns ... e.g. 2
  rows   - number of rows ...... e.g. 3
  scaFac - scale factor ........ e.g. 1.2
  scaUni - scale units ......... e.g. "nm"
  barWid - bar width (units) ... e.g. 100
  barHt  - bar ht px ........... e.g. 9
  barFnt - bar font ............ e.g. 48
  barCol - bar color ........... e.g. "White"
  barLoc - bar location ........ e.g. "Lower Right"
  """
  s1  = "Grid/Collection stitching"
  s2a = "type=[Grid: column-by-column] order=[Down & Right                ] "
  s2b = "grid_size_x=%g grid_size_y=%g tile_overlap=0 first_file_index_i=1 directory=%s" % (cols, rows, tifDir)
  s2c = " file_names=tile-{i}.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] "
  s2d = "regression_threshold=0.30 max/avg_displacement_threshold=2.50 "
  s2e = "absolute_displacement_threshold=3.50 computation_parameters=[Save memory (but be slower)] "
  s2f = "image_output=[Fuse and display] use"
  
  s2 = s2a + s2b +s2c + s2d +s2e
  # print(s2)
  IJ.run(s1, s2)
  imp = WindowManager.getCurrentImage()
  IJ.run("RGB Color")
  imp.close()
  imp = WindowManager.getCurrentImage()
  s3 = "distance=1 known=%f unit=%s" % (scaFac, scaUni)
  IJ.run("Set Scale...", s3)
  s4 = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barWid, barHt, barFnt, barCol, barLoc)
  IJ.run("Add Scale Bar", s4) 

stitchMaps(imgDir, x, y, scale, units, 100, 9, pts, barCol, "Lower Right")

# Get the final map 
imp = WindowManager.getCurrentImage()
outDir = edsDir + relOut
ensureDir(outDir)
outPth = outDir + "/" + outNam
print(outPth)
IJ.saveAs(imp, "PNG", outPth)
