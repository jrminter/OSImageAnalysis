# showJpegProb.py
#
# A reproducible example showing the problem with JPEG images
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-03  JRM 0.1.00  Converted C. Reudin's IJM macro

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ
from ij.plugin import ImageCalculator

# start clean
IJ.run("Close All","")

IJ.run("Boats (356K)")
ori = IJ.getImage()
ori.setTitle("original")
IJ.run(ori, "Out [-]", "")

IJ.run(ori, "Duplicate...", " ")
dup = IJ.getImage()
IJ.run(dup, "Out [-]", "")
IJ.run(dup, "Save As JPEG... [j]", "jpeg=85")
IJ.run(dup, "Revert", "");
dup.setTitle("JPEG")

IJ.run(ori, "32-bit", "")
ori.show()
IJ.run(dup, "32-bit", "")
dup.show()

ImageCalculator().run("Subtract", ori, dup)
dif = IJ.getImage()
dif.setTitle("difference")
# IJ.run(dif, "viridis", "");
dif.show()
