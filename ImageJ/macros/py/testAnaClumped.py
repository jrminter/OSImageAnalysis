from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from math import sqrt
from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

orig = IJ.getImage()
orig.setTitle("orig")
print(orig.getShortTitle())
iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
print(iZero)
rt = jmg.anaParticlesWatershed(orig, strThrMeth="method=Otsu white", bFillHoles=True, minPx=7, maxPx=150)
nMeas = rt.getCounter()
print(nMeas)



