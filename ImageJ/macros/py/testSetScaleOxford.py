# testSetScaleOxford.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-26  JRM 0.1.00  Initial prototype
# 
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')


from ij import IJ

sbWid  = 0.5
sbFont = 24
sbCol  = "White"
sbPos  = "Upper Right"
sbHt   = 6


imgFwUnits = 5.79
units = IJ.micronSymbol + "m"

imp = IJ.getImage()
wid = imp.getWidth()
IJ.run(imp, "Enhance Contrast", "saturated=0.35")
IJ.run(imp, "RGB Color", "")
strScale =  "distance=%g known=%g pixel=1 unit=%s" % (wid, imgFwUnits, units)
IJ.run(imp, "Set Scale...", strScale)

strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (sbWid, sbHt, sbFont, sbCol, sbPos)
IJ.run(imp, "Add Scale Bar", strBar);
