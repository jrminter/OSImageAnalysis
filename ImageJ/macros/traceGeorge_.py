# traceGeorge_.py
#
# Find the boundary points from a high contrast image
# of George Washington. Image credit: Roger Button
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-0t  JRM 0.1.00  Initial example 

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
from ij import WindowManager

bCleanup = True
gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images"
strImg = gitDir + relImg + "/George.tif"
strTxt = gitDir + relImg + "/George.txt"
  
# 1. Open an image 
impRaw =  IJ.openImage(strImg)
impRaw.show()
IJ.run("Find Edges")
IJ.run("Skeletonize (2D/3D)")
IJ.run("Find Connected Regions", "allow_diagonal display_one_image display_results regions_for_values_over=100 minimum_number_of_points=1 stop_after=-1")
strSaveCoord = "background=0 save=%s" %  strTxt
IJ.run("Save XY Coordinates...", strSaveCoord)
# Get the final map 
impCon = WindowManager.getCurrentImage()
impRaw.changes=False
impRaw.close()
resWin = WindowManager.getWindow("Results")
resWin.dispose()
# logWin = WindowManager.getWindow("Log")
# logWin.dispose()
if bCleanup:
  impCon.changes=False
  impCon.close()
  