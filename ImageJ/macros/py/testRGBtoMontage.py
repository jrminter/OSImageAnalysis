# testRGBtoMontage
# Test a jython function to make a montage of the R,G,B channels, and the RGB image
# This is a replacement for the RGB_to_montage plug-in that does not seem to still exist
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-22  JRM 0.1.00  replacement for the RGB_to_montage plug-in

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
import jmFijiGen as jmg

# make an input RGB image

IJ.run("Fluorescent Cells (400K)")
imp = IJ.getImage()
IJ.run(imp, "RGB Color","")
imp.close()
rgb = IJ.getImage()

a = jmg.RGBtoMontage(rgb)



