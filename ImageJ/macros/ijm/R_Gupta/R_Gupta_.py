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

# create a gray image fo redirect...
impGbare = impG.duplicate()
impGbare.setTitle("green_channel")
impGbare.show()

impG.setRoi(OvalRoi(22,12,334,337))
impG.show()

w = impG.getWidth()
h = impG.getHeight()
print(w, h)
sp = ByteProcessor(w,h)
blank = ImagePlus("blank", sp)
pix = blank.getProcessor().getPixels()
for i in range(len(pix)):
   pix[i] = -1

blank.show()

IJ.selectWindow("original (green)");
IJ.run("Copy")
IJ.selectWindow("blank")
IJ.run("Paste")

blank.show()
impBlank = IJ.getImage()
IJ.setAutoThreshold(impG, "Default")
Prefs.blackBackground = False
IJ.run(impBlank, "Convert to Mask", "")
IJ.run("Watershed")
#
# My Original
#
# IJ.run("Set Measurements...", "area mean integrated add redirect=Picture1.jpg decimal=3")
# IJ.run(impBlank, "Analyze Particles...", "  show=Outlines display exclude summarize")

# From recorder

# IJ.run("Set Measurements...", "area mean integrated add redirect=Picture1.jpg decimal=3")
# IJ.run(impBlank, "Analyze Particles...", "  show=Outlines display exclude summarize")

