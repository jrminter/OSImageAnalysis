# testSetScaleOxford.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-26  JRM 0.1.00  Initial prototype
# 2015-01-27  JRM 0.1.10  More control and write a dummy to get parameters
#                         set the first time

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')


from ij import IJ
from ij.gui import PointRoi

sbWid  = 0.5
sbFont = 24
sbCol  = "White"
# loc for scale bar. if sbPtX=None will use sbPos
sbPtX  =  50
sbPtY  =  720
sbPos  = "Lower Right"
sbHt   = 6

bAdjustContrast = False
imgFwUnits = 5.79
units = IJ.micronSymbol + "m"

imp = IJ.getImage()
wid = imp.getWidth()
if bAdjustContrast == True:
  IJ.run(imp, "Enhance Contrast", "saturated=0.35")
IJ.run(imp, "RGB Color", "")
strScale =  "distance=%g known=%g pixel=1 unit=%s" % (wid, imgFwUnits, units)
IJ.run(imp, "Set Scale...", strScale)

# burn a scale bar
# first make a dummy image
dummy = imp.duplicate()
if sbPtX == None:
  strSB = "width=%g height=%g font=%g color=%s location=[%s] bold" % (sbWid, sbHt, sbFont, sbCol, sbPos)
else:
  imp.setRoi(PointRoi(sbPtX, sbPtY))
  dummy.setRoi(PointRoi(sbPtX, sbPtY))
  strSB = "width=%g height=%g font=%g color=%s location=[At Selection] bold" % (sbWid, sbHt, sbFont, sbCol )

# first burn a scale bar in the dummy image to make sure changes are written
IJ.run(dummy, "Add Scale Bar", strSB)
# close the dummy
dummy.changes = False
dummy.flush()

# now burn the scale bar we really want...
IJ.run(imp, "Add Scale Bar", strSB)
# now set an out-of-bounds point roi to get rid of the cross
imp.setRoi(PointRoi(-10, -10))

