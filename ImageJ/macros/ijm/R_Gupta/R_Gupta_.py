# R_Gupta_.py
#
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-05-10  JRM 0.1.00  initial py script based on RG plugin
#                         
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ, Prefs,WindowManager, ImagePlus
from ij.gui import OvalRoi
from ij.process import ImageStatistics, ByteProcessor
from ij.measure import Measurements
from array import zeros

orig = IJ.getImage()
name = orig.getTitle()
print(name)

wName = "original"
work = orig.duplicate()
work.setTitle(wName)
work.show()
IJ.run("Split Channels")
imgNamR = wName + " (red)"
print(imgNamR)
impR = WindowManager.getImage(imgNamR)
impR.close()
imgNamB = wName + " (blue)"
impB = WindowManager.getImage(imgNamB)
print(imgNamB)
impB.close()

imgNamG = wName + " (green)"
impG = WindowManager.getImage(imgNamG)
impG.show()
impG.setRoi(OvalRoi(22,12,334,337))

w = impG.getWidth()
h = impG.getHeight()
print(w, h)
sp = ByteProcessor(w,h)
blank = ImagePlus("blank", sp)
pix = blank.getProcessor().getPixels()
for i in range(len(pix)):
   pix[i] = -1

blank.show()
IJ.setAutoThreshold(impG, "Default")
Prefs.blackBackground = False;

impG.show()
impG.setRoi(OvalRoi(22,12,334,337))
IJ.run("Copy")
blank.show()


