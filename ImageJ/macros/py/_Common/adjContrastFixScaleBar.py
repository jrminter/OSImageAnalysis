from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
adjContrastFixScalebar.py

J. R. Minter

Adjust the contrast, convert to RGB, and burn a scale bar

CCA licence
  date      who   ver   comment
----------  ---  ------ -----------------------------------------------------
2017-04-10  JRM  0.0.10  Initial
2017-04-12  JRM  0.0.11  Pep8 and codecs at top
"""

# common to change...
bCvtToNm = True
barW     = 100.          # default bar width in nm or default units (um)
gSatFac  = 0.05

# less common to change...
barH =  6           # bar height, pts
barF = 24           # bar font, pts
barC = "White"      # bar color
barL= "Lower Right" # bar location


# should not need to change below here...
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg

mu = IJ.micronSymbol
scaUm    = mu + "m"

orig = IJ.getImage()
if orig != None:
    strName = orig.getShortTitle()
    orig.setTitle(strName)
    cal = orig.getCalibration()
    u = cal.getUnit()
    pw = cal.pixelWidth
    if bCvtToNm:
        if(u == scaUm):
            pw = cal.pixelWidth
            ph = cal.pixelHeight
            pw *= 1000.0
            ph *= 1000.0
            str1 = "channels=1 slices=1 frames=1 unit=nm "
            str2 = "pixel_width=%.5f pixel_height=%.5f voxel_depth=%.5f" % (pw, ph, pw) 
            IJ.run(orig,"Properties...", str1+str2)
            orig.updateAndDraw()
            
    strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
    # a hack to get the scale bars to work reliably
    foo = orig.duplicate()
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)
    foo.close()
    
    sArgSat = "saturated=%.2f" % gSatFac
    IJ.run(orig, "Enhance Contrast", sArgSat)
    IJ.run(orig, "RGB Color", "")
    IJ.run(orig, "Add Scale Bar", strBar)
    orig.show()



