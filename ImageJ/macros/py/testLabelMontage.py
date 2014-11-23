# 02-montage-qm-nnnnn-sampleID-nnkV-map1
# Make montage from qm-nnnnn-sampleID-nnkV-map1
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-22  JRM 0.1.00  test auto-labelling a montage

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
import jmFijiGen as jmg


raw = IJ.getImage()
# map fills row-by row left to right
lName = ["C", "N","O","Cu", "P", "Cl", "Pd", "Ag", "ROI"]
nCol = 3
nRow = 3



a = jmg.labelMontage(raw, lName, nCol, nRow, w0=12, h0=8, font=28)
