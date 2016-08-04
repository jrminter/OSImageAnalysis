# testReadPrefs.py.py
#
# J. R. Minter
#
#
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-08-04  JRM  Read prefd


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg


def resetLastMeasureCount():
    Prefs.set("JRM.meas.counter", 0)

def GetLastMeasureCount():
    myCount = Prefs.get("JRM.meas.counter", int(-1))
    if myCount < 0:
        # it was not set, so set it to zero
        resetLastMeasureCount()
        return 0
    else:
        myCount = int(myCount)
        return myCount

def setLastMeasureCount(count):
    count = int(count)
    Prefs.set("JRM.meas.counter", count)

resetLastMeasureCount()
setLastMeasureCount(4.0)
myCount = GetLastMeasureCount()
print(myCount)



# Prefs.set("Last.Image.Dir", basePath)

