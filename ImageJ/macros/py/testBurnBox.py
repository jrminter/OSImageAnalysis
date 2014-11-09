# testBurnBox.py
#
# test the burnBox function imported from jmFijiGen
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  ----------------------------------------------------
# 2014-11-07  JRM 0.1.00  initial test. Burns a green box into the blobs image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
import jmFijiGen as jmg

IJ.run("Blobs (25K)")
lRoi = [50, 50, 128, 128]
raw = IJ.getImage()
jmg.burnBox(raw, lRoi, col="green", wid=4)
