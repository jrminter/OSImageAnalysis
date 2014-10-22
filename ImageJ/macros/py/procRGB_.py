# procRGB_.py
#
# proess an RGB image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-21  JRM 0.1.00  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg
from ij import IJ
from ij import WindowManager
from ij.plugin import ChannelSplitter

from script.imglib.math import Compute, Divide, Multiply, Subtract  
from script.imglib.algorithm import Gauss, Scale2D, Resample  
from script.imglib import ImgLib 


def flatFieldCorrectRGB(impImg, impFF, scaFac=0.5):
  cs = ChannelSplitter()
  impImg.show()
  [rImg, gImg, bImg] = cs.split(impImg)
  impImg.changes = False
  impImg.close()
  rImg.hide()
  gImg.hide()
  bImg.hide()
  
  
  rImg.show()
  IJ.run("32-bit")
  # rImg = WindowManager.getCurrentImage()
  rImg.hide()
  
  gImg.show()
  IJ.run("32-bit")
  # gImg = WindowManager.getCurrentImage()
  gImg.hide()
  
  bImg.show()
  IJ.run("32-bit")
  # bImg = WindowManager.getCurrentImage()
  bImg.hide()

  impFF.show()
  [rBkg, gBkg, bBkg] = cs.split(impFF)
  impFF.changes = False
  impFF.close()
  rBkg.hide()
  gBkg.hide()
  bBkg.hide()
  
  rBkg.show()
  img = ImgLib.wrap(rBkg)
  
  gain = Resample(Gauss(Scale2D(img, scaFac), 20), img.getDimensions())
  rBkg = ImgLib.wrap(gain)
  IJ.run("32-bit")
  rBkg.hide()

  gBkg.show()
  img = ImgLib.wrap(gBkg)
  gBkg.changes = False
  gBkg.close()
  gain = Resample(Gauss(Scale2D(img, scaFac), 20), img.getDimensions())
  gBkg = ImgLib.wrap(gain)
  IJ.run("32-bit")
  gBkg.hide()

  bBkg.show()
  img = ImgLib.wrap(bBkg)
  bBkg.changes = False
  bBkg.close()
  gain = Resample(Gauss(Scale2D(img, scaFac), 20), img.getDimensions())
  bBkg = ImgLib.wrap(gain)
  IJ.run("32-bit")
  bBkg.show()

  
  



imgDir  = os.environ['IMG_ROOT']
relImg  = "/efi-test"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg = imgDir + relImg + "/50X-2-EDF.tif"
strFF  = imgDir + relImg + "/50X-2-FF.tif"

# 1. Open an image and it's flat field
impExp = IJ.openImage(strImg)
impBkg  =  IJ.openImage(strFF)

flatFieldCorrectRGB(impExp, impBkg)









