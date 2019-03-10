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


import os

from java.awt import Color
from ij import IJ, ImagePlus
from ij.gui import TextRoi, Overlay

def labelImage(imp, lLab, lX, lY, font=24, col=Color.WHITE):
  l = len(lLab)
  # make a copy
  res = imp.duplicate()
  # let's create an array of text rois
  ol = Overlay()
  for i in range(l):
    tr = TextRoi(lX[i], lY[i]-(font/2), lLab[i])
    tr.setColor(col)
    tr.setFont("SanSerif", font, 1) 
    tr.setJustification(TextRoi.CENTER)
    tr.setAntialiased(True)
    ol.add(tr)
  res.show()
  res.setOverlay(ol)
  res.updateAndRepaintWindow()
  return res

homDir = os.environ['HOME']
imgPath = homDir + '/git/OSImageAnalysis/images/blobs.gif'
raw = IJ.openImage(imgPath)
raw.show()

lX   = [ 74,  90, 180 ]
lY   = [ 41, 160, 180 ]
lLab = ["1", "2", "3" ]

labelImage(raw, lLab, lX, lY) 



