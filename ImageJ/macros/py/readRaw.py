# ReadRaw.py
#
# A script to import a RAW image
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-03-23  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import time
from ij import IJ
import jmFijiGen as jmg

#
# Crunch
imgDir = "D:/Data/images/key-test/EE-569/raw/"
outDir = "D:/Data/images/key-test/EE-569/png/"
#
# MacBook, Pro
# imgDir = "/Users/jrminter/dat/images/key-test/EE-569/raw/"
# outDir = "/Users/jrminter/dat/images/key-test/EE-569/png/"

imgFil  = "parrot_CFA"
imgWid  = 424
imgHt   = 636
# imgTyp  = "[24-bit RGB]"
imgTyp  = "[8-bit]"

strImport = "open=%s" %  (imgDir)
strImport += "%s.raw " %  (imgFil)
strImport += "image=%s " %  (imgTyp)
strImport += "width=%g " %  (imgWid)
strImport += "height=%g " %  (imgHt)


print(strImport)

IJ.run("Raw...", strImport);

orig = IJ.getImage()
orig.show()
outPth = outDir + imgFil + ".png"
IJ.saveAs(orig, "PNG", outPth)

time.sleep(1)
orig.close()



