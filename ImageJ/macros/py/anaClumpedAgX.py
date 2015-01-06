# anaClumpedAgX.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-07-26  JRM 0.1.00  initial prototype development. Note that Fiji 
#                         can read .dm3 files directly. N.B. This version
#                         adds the environment variable 'RPT_ROOT'
# 2014-09-30  JRM 0.1.10  Moved some code to jmFijiGen and edit for ImageJ2
# 2015-01-04  JRM 0.2.00  Changed to call anaParticlesWatershed() from
#                         jmFijiGen and to compute contrast
# 2015-01-05  JRM 0.2.10  Added image and particle number and fixed scale bar
# 2015-01-06  JRM 0.2.20  Fixed Contrast
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from math import sqrt
from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

imgDir  = os.environ['IMG_ROOT']
rptDir  = os.environ['RPT_ROOT']
relImg  = "/test/clumpAgX"
sampID  = "qm-03966-KJL-031"
nmPerPx = 1.213
minCirc = 0.5
minSize = 1.0e1
maxSize = 1.0e6

barW    =    100  # bar width, nm
barH    =      6  # bar height, pts
barF    =     28  # bar font, pts
barC    = "Black" # bar color

strBar = "width=%g height=%g font=%g color=%s location=[Lower Right] bold" % (barW, barH, barF, barC)

sImgPath = imgDir + relImg + "/" + sampID + "/"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)
sRptCsvPath = sRptPath + sampID + ".csv"
sRptImgPath = sRptPath + "png/"
jmg.ensureDir(sRptImgPath)

# create empty output vectors for results
imgOut = []
parOut = []
ecdOut = []
conOut = []
cirOut = []
rndOut = []
solOut = []
arOut  = []

query = sImgPath + "*.dm3"
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
  i += 1
  orig = ImagePlus(fi)
  strName = os.path.basename(fi)
  strName = strName.split('.')[0]
  lStr =  strName.split('-')
  l = len(lStr)
  strNum = lStr[l-1]
  orig.setTitle(strNum)
  if i == 1:
    # a hack to get the scale bars to work reliably
    foo = orig.duplicate()
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)
  iZero = jmg.findI0(orig, maxSearchFrac=0.5, chAvg=5)
  # print(iZero)
  rt = jmg.anaParticlesWatershed(orig, minPx=30)
  nMeas = rt.getCounter()
  
  nCols = rt.getLastColumn()
  lArea   = rt.getColumn(rt.getColumnIndex("Area"))
  lMode   = rt.getColumn(rt.getColumnIndex("Mode"))
  # lPeri   = rt.getColumn(rt.getColumnIndex("Perim."))
  # lMaj    = rt.getColumn(rt.getColumnIndex("Major"))
  # lMin    = rt.getColumn(rt.getColumnIndex("Minor"))
  lCirc   = rt.getColumn(rt.getColumnIndex("Circ."))
  # lFeretX = rt.getColumn(rt.getColumnIndex("FeretX"))
  # lFeretY = rt.getColumn(rt.getColumnIndex("FeretY"))
  lAspRat = rt.getColumn(rt.getColumnIndex("AR"))
  lRound  = rt.getColumn(rt.getColumnIndex("Round"))
  lSolid  = rt.getColumn(rt.getColumnIndex("Solidity"))
  for j in range(len(lArea)):
    imgOut.append(i)
    parOut.append(j+1)
    ecd = 2.0*sqrt(lArea[j]/3.1415926)
    ecdOut.append(ecd)
    con = 1.0-(lMode[j]/iZero)
    conOut.append(con)   
    cirOut.append(lCirc[j])
    arOut.append(lAspRat[j])
    rndOut.append(lRound[j])
    solOut.append(lSolid[j])
    
    
  orig.show()
  outPth = sRptImgPath + strName + ".png"
  # burn a scale bar and save the image
  IJ.run(orig, "RGB Color", "")
  IJ.run(orig, "Add Scale Bar", strBar)
  IJ.saveAs(orig, "PNG", outPth)
  orig.changes = False
  orig.close()

  print("%d particles detected in image %s" % (nMeas, strNum))

# prepare the output file
f=open(sRptCsvPath, 'w')
strLine = 'img, part, ecd.nm, contrast, circ, a.r, round, solidity\n'
f.write(strLine)
for i in range(len(ecdOut)):
  strLine = "%d, %d, %.2f, %.4f, %.4f, %.4f, %.4f, %.4f\n" % (imgOut[i], parOut[i], ecdOut[i],  conOut[i], cirOut[i], arOut[i], rndOut[i], solOut[i] )
  f.write(strLine)

f.close()

toc = time.time()

elapsed = toc - tic

print("completed in %g sec" % elapsed )

# All with Oracle JDK 1.7.0_71
#  54 sec on jrmFastMac   - Yosemite 16 GB RAM i7 4 cores MacBookPro11,3 2.3 GHz
#  32 sec on crunch       - Win7-64  16 GB RAM i7-3370 8 cores           3.4 GHz
#  46 sec on ROCPW6C6XDN1 - Win7-64  16 GB RAM Core Duo E8500 CPU        3.0 GHz
#  48 sec on ROCTL185TXY1 - Win7-32   4 GB RAM i5-3340M CPU              2.7 GHz

  