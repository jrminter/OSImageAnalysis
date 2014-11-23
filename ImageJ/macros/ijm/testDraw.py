# testLabelImage
# Test a jython function label an image
# This works now for a single ROI
#
# TO DO: take lists of x, y, and labels
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-22  JRM 0.1.00  Add annotations to an image


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from java.awt import Color
from ij import IJ, ImagePlus
from ij.gui import TextRoi, Overlay

def labelImage(imp, label, x, y, font=24, col=Color.WHITE):
  tr = TextRoi(10, 0, label)
  tr.setColor(col)
  tr.setFont("SanSerif", font, 1) 
  tr.setJustification(TextRoi.CENTER)
  tr.setAntialiased(True)
  ol = Overlay()
  ol.add(tr)
  imp.setOverlay(ol)
  imp.updateAndRepaintWindow()
  imp.show()
  return imp


raw = IJ.getImage()

labelImage(raw, "R", 3, 10) 



