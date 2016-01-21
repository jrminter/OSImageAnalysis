# anaClumpedMatte.py
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-01-21  JRM 0.1.00  Adaped from anaClumpedAgX

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from math import sqrt, pi
from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg


tic = time.time()

imgDir  = os.environ['IMG_ROOT']
rptDir  = os.environ['RPT_ROOT']
relImg  = "/QM16-04-01A-Shevlin" 
sampID  = "qm-04595-307-85120-3"
umPerPx = 0.3647
minCirc = 0.6
maxAR   = 1.25

minDiaUm =  7.0
maxDiaUm = 20.0

minRad = 0.5*minDiaUm
maxRad = 0.5*maxDiaUm
minArea = pi*minRad*minRad
maxArea = pi*maxRad*maxRad

barW    =     20  # bar width, um
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
cirOut = []
rndOut = []
solOut = []
arOut  = []

query = sImgPath + "*.tif"
print(query)
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
  i += 1
  orig = ImagePlus(fi)
  orig = jmg.calibImageDirect(orig, umPerPx, units=-6)
  strName = orig.getShortTitle()
  strNum = strName.split('IMAGE')[1]
  iNum = int(strNum)
  strName = "%s-%02d" % (sampID, iNum ) 
  orig.setTitle(strName)
  orig.show()
  if i == 1:
    # a hack to get the scale bars to work reliably
    foo = orig.duplicate()
    IJ.run(foo, "RGB Color", "")
    IJ.run(foo, "Add Scale Bar", strBar)

  rt = jmg.anaParticlesWatershed(orig, strThrMeth="method=Otsu white", bFillHoles=True, minPx=minArea, maxPx=maxArea, minCirc=minCirc, maxAR=maxAR)
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
  k = 0
  for j in range(len(lArea)):
  	if lAspRat[j] <= maxAR:
  		k += 1
    	imgOut.append(iNum)
    	parOut.append(k)
    	ecd = 2.0*sqrt(lArea[j]/3.1415926)
    	ecdOut.append(ecd)
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
strLine = 'img, part, ecd.um, circ, a.r, round, solidity\n'
f.write(strLine)
for k in range(len(ecdOut)):
  strLine = "%d, %d, %.2f, %.4f, %.4f, %.4f, %.4f\n" % (imgOut[k], parOut[k], ecdOut[k], cirOut[k], arOut[k], rndOut[k], solOut[k] )
  f.write(strLine)

f.close()



toc = time.time()

elapsed = toc - tic
print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )

# All with Oracle JDK 1.6
       

  