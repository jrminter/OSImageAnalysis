# procRGB_.py
#
# proess an RGB image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-21  JRM 0.1.00  Initial prototype
# 2014-10-22  JRM 0.1.10  Finally got to work

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import time
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator


def flatFieldCorrectRGB(impImg, impFF, sigma=100):
  strSigma = "sigma=%g" % sigma
  name = impImg.getShortTitle()
  cs = ChannelSplitter()
  impImg.show()
  [rImg, gImg, bImg] = cs.split(impImg)
  impImg.changes = False
  impImg.close()
  rImg.setProcessor(rImg.getProcessor().convertToFloat()) 
  gImg.setProcessor(gImg.getProcessor().convertToFloat()) 
  bImg.setProcessor(bImg.getProcessor().convertToFloat()) 

  impFF.show()
  [rBkg, gBkg, bBkg] = cs.split(impFF)
  impFF.changes = False
  impFF.close()
  rBkg.setProcessor(rBkg.getProcessor().convertToFloat())
  rBkg.show()
  IJ.run("Gaussian Blur...", strSigma)
  rBkg.hide()
  
  gBkg.setProcessor(gBkg.getProcessor().convertToFloat())
  gBkg.show()
  IJ.run("Gaussian Blur...", strSigma)
  gBkg.hide()
  
  bBkg.setProcessor(bBkg.getProcessor().convertToFloat())
  bBkg.show()
  IJ.run("Gaussian Blur...", strSigma)
  bBkg.hide()

  ic = ImageCalculator()

  rCor = ic.run("Divide create 32-bit", rImg, rBkg)
  rCor.setTitle("rCor")
  rCor.show()
  win = WindowManager.getWindow("rCor")
  WindowManager.setCurrentWindow(win)
  IJ.run("8-bit")
  
  gCor = ic.run("Divide create 32-bit", gImg, gBkg)
  gCor.setTitle("gCor")
  gCor.show()
  win = WindowManager.getWindow("gCor")
  WindowManager.setCurrentWindow(win)
  IJ.run("8-bit")
 
  bCor = ic.run("Divide create 32-bit", bImg, bBkg)
  bCor.setTitle("bCor")
  bCor.show()
  win = WindowManager.getWindow("bCor")
  WindowManager.setCurrentWindow(win) 
  IJ.run("8-bit")
  
  IJ.run("Merge Channels...", "c1=[rCor] c2=[gCor] c3=[bCor] create")
  impComp = WindowManager.getCurrentImage()
  IJ.run("RGB Color")
  impComp.changes = False
  impComp.close()

  impSc = WindowManager.getCurrentImage()
  impSc.setTitle(name + "-sc")
  impSc.updateAndDraw()

  return impSc


  


imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1/ff"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg = imgDir + relImg + "/sis-efi.tif"
print(strImg)
strFF  = imgDir + relImg + "/gain.tif"

# 1. Open an image and it's flat field
impExp = IJ.openImage(strImg)
impExp.show()
impBkg  =  IJ.openImage(strFF)

impSc = flatFieldCorrectRGB(impExp, impBkg)









