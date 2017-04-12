from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
makePngFromCalibTifWithSb.py

J. R. Minter

Process a folder of calibrated .tif files and burn scale bars

CCA licence

 date       who   ver     comment
----------  ---  ------  -----------------------------------------------
2016-02-02  JRM  0.0.10  Works with a directory chooser
2016-02-24  JRM  0.0.11  Added some error handling
2017-02-20  JRM  0.0.12  Can change to nm. Consistent spacings...
2017-04-12  JRM  0.0.13  PEP8 and move codecs to top
"""


bVerbose       = False
gSatFac        =   0.001        # Gray level saturation factor
bConvertToNm   = True           # Change to nm
barW           = 50.0           # bar width in nm or default units (um)
barH           =  6             # bar height, pts
barF           = 24             # bar font, pts
barC           = "White"        # bar color
barL           = "Lower Right"  # bar location
bDoTiltCorrect = False          # correct for tilt correction
bSetGrayLevels = False          # if True, will set gLo and gHi

# If True, these will be used. Set as needed for a given series.
gLo = 0
gHi = 22000

# Should not need to change below here!

import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg

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
    strName = strName.split('.')[0]
    orig.setTitle(strName)
    
    if bVerbose:
        print(pw)
    orig = ImagePlus(fi)
    strName = os.path.basename(fi)
    strName = strName.split('.')[0]
    orig.setTitle(strName)
    cal = orig.getCalibration()
    u = cal.getUnit()
    pw = cal.pixelWidth
    if bConvertToNm:
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
    if (bSetGrayLevels == True):
        IJ.setMinAndMax(foo, gLo, gHi)
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)
    foo.close()

    if (bSetGrayLevels == True):
        IJ.setMinAndMax(orig, gLo, gHi)
    else:
        sArgSat = "saturated=%.2f" % gSatFac
        IJ.run(orig, "Enhance Contrast", sArgSat)

    if(bDoTiltCorrect == True):
        orig = jmg.correctForeshortening(orig, tiltDeg)
        orig = IJ.getImage()
    
    IJ.run(orig, "RGB Color", "")
    IJ.run(orig, "Add Scale Bar", strBar)
    orig.show()
    outPth = sPngPath + strName + ".png"
    IJ.saveAs(orig, "PNG", outPth)
    time.sleep(1)
    orig.close()

toc = time.time()

elapsed = toc - tic

print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )
