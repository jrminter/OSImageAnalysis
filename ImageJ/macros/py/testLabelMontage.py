# 02-montage-qm-nnnnn-sampleID-nnkV-map1
# Make montage from qm-nnnnn-sampleID-nnkV-map1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-22  JRM 0.1.00  test auto-labelling a montage

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from java.awt import Color
from ij import IJ
from ij.gui import Roi, TextRoi, Overlay
import jmFijiGen as jmg

def labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24, col=Color.WHITE):
  """labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24, col=Color.WHITE)
  Label a montage in the overlay
  Inputs:
  imp     - the ImagePlus of the montage to label
  lLabels - a list of labels to write into the overlay
  cols    - the number of columns in the montage
  rows    - the number of rows in the montage
  w0      - the x offset for the label (defaults to 12 px)
  h0      - the y offset for the label (defaults to  2 px)
  font    - the size of the font (pts, defaults to 24)
  col     - color of text. Default to Color.WHITE
  Returns
  an ImagePlus with a labeled, duplicate of the input image
  """
  print(cols,rows)
  wBase = imp.getWidth()/cols
  hBase = imp.getHeight()/rows
  print(wBase, hBase)
  l = len(lLabels)
  xt = 0
  y = 0
  # make a copy
  res = imp.duplicate()
  # let's create an array of text rois
  ol = Overlay()
  for i in range(l):
    x = (i % cols+1)-1
    if x < xt:
      y += 1
    xt = x
    xL = x * wBase + w0
    yL = y * hBase + h0
    print(xL,yL)
    tr = TextRoi(xL, yL, lLabels[i])
    tr.setColor(col)
    tr.setFont("SanSerif", font, 1) 
    tr.setJustification(TextRoi.CENTER)
    tr.setAntialiased(True)
    ol.add(tr)
  res.show()
  res.setOverlay(ol)
  res.updateAndRepaintWindow()
  return res


raw = IJ.getImage()
# map fills row-by row left to right
# lAnn = ["C", "N","O","Cu", "P", "Cl", "Pd", "Ag", "ROI"]
# nCol = 3
# nRow = 3
lAnn  = ["O", "Cu", "P", "Cl", "Pd", "ROI"]
nCol = 3
nRow = 2



a = labelMontage(raw, lAnn, nCol, nRow, w0=12, h0=8, font=28)
