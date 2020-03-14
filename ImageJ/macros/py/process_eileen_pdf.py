# process_eileen_pdfs.py
# A script to process Eileen's PDF with ImageJ
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2020-03-01  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ
from ij.io import FileSaver
import jmFijiGen as jmg

baseDir = "C:/Users/johnr/Documents/work/eileen/"
imgName = "Chapter-8-27"
imgExt = ".pdf"

inputImgFile = baseDir + imgName + imgExt

print(inputImgFile)
str2 = "choose="+baseDir+imgName+imgExt + "  scale=200 page=0"
print(str2)

IJ.run("PDF ...", str2)
imp = IJ.getImage()
IJ.setMinAndMax(120, 255, 6)
str2 = "scale one us save=" + baseDir + "proc/" + imgName + imgExt
# print(str2)

IJ.run(imp, "PDF ... ", str2)