from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
makeGrayPngFromCalibTifWithSb.py

J. R. Minter

Process a folder of calibrated .tif files and burn scale bars
. This
version computes the cumulative gray level histogram and sets the
lower display limit to zero and the upper display limit to a specified
fraction of the cumulative histogram. For most images a factor very close
to 1 (i.e. 0.99995) is appropriate. Some images with charging can use a
lower factor. The png file is written as an RGB image.

CCA licence

   date     who  ver   comment
----------  ---  ----- -------------------------------------------------
2016-02-02  JRM  0.0.10 Works with a directory chooser
2016-02-24  JRM  0.0.11 Added some error handling
2016-09-27  JRM  0.0.12 Permit . (other than file ext) in file names
2017-04-12  JRM  0.0.13 Move codecs to top, put what changes near top
                        Set for PEP8
2017-10-27  JRM  0.0.14 Use jmg.calcMaxGrayLevelFromCumulativeHistogram
                        
"""
__revision__ = "$Id: makeGrayPngFromCalibTifWithSb.py John R. Minter 2017-10-27$"
__version__ = "0.0.14"

import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg

bDespeckle = False
bVerbose = True
barW =  1.0          # default bar width - reset in lines 127-133
barH = 6             # bar height, pts
barF = 24            # bar font, pts
barC = "White"       # bar color
barL = "Lower Right" # bar location

factor = 0.99995

bDoTiltCorrect = False


# Should not need to change below here...

tic = time.time()



mu = IJ.micronSymbol
scaUm    = mu + "m"


lastPath = Prefs.get("Last.Image.Dir", "None")
if os.path.exists(lastPath):
    os.chdir(lastPath)

dc = DirectoryChooser("Choose directory")
basePath = dc.getDirectory()

print(basePath)
Prefs.set("Last.Image.Dir", basePath)

names = []
for file in os.listdir(basePath):
    if file.endswith(".tif"):
        name = os.path.splitext(file)[0]
        names.append(name)

names.sort()

for name in names:
    path = basePath + os.sep + name + ".tif"
    if bVerbose:
        print(path)

sPngPath = basePath + "/png/"

if bVerbose:
    print(basePath)

jmg.ensureDir(sPngPath)

mu = IJ.micronSymbol
scaUm    = mu + "m"


query = basePath + "*.tif"

if bVerbose:
    print(query)

lFiles = glob.glob(query)
i = 0
for fi in lFiles:
    i += 1
    fi = fi.replace("\\", "/")
    fi = fi.replace("//", "/")
    if bVerbose:
        print(fi)
    orig = ImagePlus(fi)
    strName = os.path.basename(fi)
    strName = strName.rsplit('.', 1)[:-1][0]
    print(strName)
    orig.setTitle(strName)
    orig.show()
    cal = orig.getCalibration()
    u = cal.getUnit()
    pw = cal.pixelWidth
    if bVerbose:
        print(pw)
    if u == scaUm:
        if (pw <= 0.02):
            barW =  0.10  # bar width, microns
        elif (pw < 0.06):
            barW =  1.0   # bar width, microns
        else:
            barW =  10.0

    strBar = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barW, barH, barF, barC, barL)
    # a hack to get the scale bars to work reliably
    foo = orig.duplicate()
    bd = orig.getBitDepth()
    if(bd==16):
        thr = jmg.calcMaxGrayLevelFromCumulativeHistogram(foo, factor)
        if bVerbose:
            print(thr)
        foo.updateImage()
        foo.updateAndRepaintWindow()
        
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)
    foo.changes = False
    foo.close()
    bd = orig.getBitDepth()
    if(bd==16):
        thr = jmg.calcMaxGrayLevelFromCumulativeHistogram(orig, factor)
        if bVerbose:
            print(thr)
        orig.updateImage()
        orig.updateAndRepaintWindow()

    if(bDoTiltCorrect == True):
        orig = jmg.correctForeshortening(orig, tiltDeg)
        orig = IJ.getImage()
    
    IJ.run(orig, "RGB Color", "")
    IJ.run(orig, "Add Scale Bar", strBar)
    orig.show()
    outPth = sPngPath + strName + ".png"
    IJ.saveAs(orig, "PNG", outPth)
    time.sleep(1)
    
    orig.changes = False
    orig.close()
