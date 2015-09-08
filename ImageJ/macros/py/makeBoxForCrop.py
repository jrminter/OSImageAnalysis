# makeBoxForCrop.py
# A script to crop a series of images
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-09-03  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ

imp = IJ.getImage()

x0 = 0
y0 = 200
wd = imp.getWidth()
ht = 340;

IJ.run("Colors...", "foreground=black background=black selection=green");
IJ.makeRectangle(x0, y0, wd, ht);
