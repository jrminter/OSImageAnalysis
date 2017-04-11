# makePngFromCalibTifWithSb.py
#
# J. R. Minter
#
# Process a folder of calibrated .tif files and burn scale bars
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-02-02  JRM  Works with a directory chooser
# 2016-02-24  JRM  Added some error handling
# 2017-02-20  JRM  Added ability to change to nm. Consistent spacings...

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg

bVerbose = False
bConvertToNm = True


tic = time.time()
# for Ambro Ferrar 2017-02-20
barW = 50.0          # default bar width in nm or default units (um)
barH =   6            # bar height, pts
barF = 24             # bar font, pts
barC = "White"        # bar color
barL= "Lower Right"   # bar location

gSatFac = 0.001

bSetGrayLevels = False
# for Nair 2016-10-31
gLo = 0
gHi = 22000 # 16-19
# gHi = 22000 # Nair 16-19
# gHi = 22500 # Nair 20-25

bDoTiltCorrect = False


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
