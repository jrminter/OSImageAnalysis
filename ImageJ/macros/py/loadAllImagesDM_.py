# loadAllImagesDM_.py
#
# Stitch Oxford EDS maps and burn scale bars
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-07  JRM 0.1.00  Load all DM3 images to burn scale bars

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time
from ij import IJ
from ij import WindowManager
from ij.gui import ImageWindow

inDir = "\\\\cm20st\\data\\images\\QM14-02-12A-Kosydar\\qm-04203-PMH1413\\dm3"
outDir = "C:\\Users\\l837410\\Documents\\work\\proj\\QM14-02-12A-Kosydar\\Sweave\\inc\\png"
for file in os.listdir(inDir):
  if file.endswith(".dm3"):
    path = inDir + "\\" + file
    # print(file)
    strLoad = "load=%s" % path
    IJ.run("DM3 Reader...", strLoad)
    IJ.run("Add Scale Bar", "width=50 height=6 font=24 color=Black location=[Lower Right] bold")
    IJ.run("RGB Color")
    l = len(file)
    name = file[0:l-4]
    print(name)
    path = outDir + "\\" + name + ".png"
    # Get the final map 
    imp = WindowManager.getCurrentImage()
    iw = ImageWindow(imp) 
    # iw.changed = False
    IJ.saveAs("PNG", path)
    iw.close()
    