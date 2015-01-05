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

sImgPath = imgDir + relImg + "/" + sampID + "/"
sRptPath = rptDir + "/" + sampID + "/"
jmg.ensureDir(sRptPath)
sRptCsvPath = sRptPath + sampID + ".csv"
sRptImgPath = sRptPath + "png/"
jmg.ensureDir(sRptImgPath)

# create empty output vectors for results
imgOut = []
ecdOut = []
conOut = []
cirOut = []
rndOut = []
solOut = []
arOut  = []

query = sImgPath + "*.dm3"
lFiles = glob.glob(query)
for fi in lFiles:
  orig = ImagePlus(fi)
  strName = os.path.basename(fi)
  strName = strName.split('.')[0]
  lStr =  strName.split('-')
  l = len(lStr)
  strNum = lStr[l-1]
  orig.setTitle(strNum)
  # orig.show()
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
    imgOut.append(strNum)
    ecd = 2.0*sqrt(lArea[j]/3.1415926)
    ecdOut.append(ecd)
    con = lMode[j]/iZero
    conOut.append(con)   
    cirOut.append(lCirc[j])
    rndOut.append(lRound[j])
    solOut.append(lCirc[j])
    arOut.append(lSolid[j])
    
  orig.show()
  outPth = sRptImgPath + strName + ".png"
  # burn a scale bar and save the image
  IJ.run(orig, "RGB Color", "")
  IJ.run(orig, "Add Scale Bar", "width=100 height=6 font=28 color=Black location=[Lower Right] bold")
  IJ.saveAs(orig, "PNG", outPth)
  orig.changes = False
  orig.close()

  print("%d particles detected in image %s" % (nMeas, strNum))

# prepare the output file
f=open(sRptCsvPath, 'w')
strLine = 'img, ecd.nm, contrast, circ, a.r, round, solidity\n'
f.write(strLine)
for i in range(len(ecdOut)):
  strLine = "%s, %.2f, %.4f, %.4f, %.4f, %.4f, %.4f\n" % (imgOut[i], ecdOut[i],  conOut[i], cirOut[i], arOut[i], rndOut[i], solOut[i] )
  f.write(strLine)

f.close()

toc = time.time()

elapsed = toc - tic

print("completed in %g sec" % elapsed )

#  56 sec on jrmFastMac (huh?)
#  32 sec on crunch
#  47 sec on ROCPW6C6XDN1

  