# RServeExample.py
# Try out RServe
# examples available here: http://www.rforge.net/Rserve/example.html
# get needed files here: http://rforge.net/Rserve/files/
# 
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-20  JRM 0.1.00  A test
from org.rosuda.REngine.Rserve import RConnection
from ij import IJ
from ij.gui import Roi, Overlay, Line
  
c = RConnection()
x = c.eval("R.version.string")
print x.asString()
imp = IJ.openImage("C:/Data/images/test/blobs.gif")
if imp == None:
  print("Error getting image")
else:
  myLine = Line(116, 204, 91, 226)
  imp.setRoi(myLine) 
  imp.show()
  print c.eval("library(Peaks)").asString()
  roi = imp.getRoi()
  if roi.getType() == Roi.LINE:
    print("a line roi")
    profile = roi.getPixels()
    c.assign("prof", profile)
    lMin = c.eval("min(prof)").asDouble()
    print(lMin)
  else:
    print ("no line found")
c.close()
