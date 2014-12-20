# -*- coding: utf-8 -*-
# jmFijiGen.py
# ImageJ Jython - J. R. Minter - 2014-09-11
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-09-11  JRM 1.1.00  First test ensureDir
# 2014-10-02  JRM 1.1.10  Added flatField
# 2014-10-04  JRM 1.1.11  Added median and removeOutliers filters from tutorial
# 2014-10-10  JRM 1.1.12  Added calibImage
# 2014-10-11  JRM 1.1.13  Added makeTmpDir, makeMontage and calibAZtecImage
# 2014-10-14  JRM 1.1.14  Added computeStats to compute mu,s, and count for a
#                         list 
# 2014-10-20  JRM 1.1.15  Added makeStackFromDir
# 2014-10-23  JRM 1.1.16  Added flatFieldCorrectRGB
# 2014-10-25  JRM 1.1.17  Added whiteBalance
# 2014-10-25  JRM 1.1.18  Added some calls to imp.flush() to clean up memory
# 2014-10-27  JRM 1.1.19  Fixed path spacer
# 2014-10-28  JRM 1.1.20  Added verbose flag to WhiteBalance 
# 2014-10-28  JRM 1.1.21  Consolidated getUnitString for DRY and added calStackZ
# 2014-10-29  JRM 1.1.22  Added smoothFlatField
# 2014-10-29  JRM 1.1.23  Added procAZtecTifMap
# 2014-10-30  JRM 1.1.24  Added vertProfileFromROI to process MAP ROIs
# 2014-11-01  JRM 1.1.25  Updated vertProfileFromROI and doCrop to work
#                         in headless mode. Many more functions to fix...
# 2014-11-03  JRM 1.1.26  Upgraded procAZtecTifMap, calStackZ
# 2014-11-06  JRM 1.1.27  Added i2b, hueDegToRGBCol, applyHueLUT
# 2014-11-09  JRM 1.1.28  Added burnBox
# 2014-11-18  JRM 1.1.29  Added findI0
# 2014-11-18  JRM 1.1.30  Fixed findI0 for 16 bit images
# 2014-11-22  JRM 1.1.31  Added RGBtoMontage and labelMontage
# 2014-11-25  JRM 1.1.32  Fixed bug in labelMontage
# 2014-11-26  JRM 1.1.33  Fixed bug in whiteBalance
# 2014-12-02  JRM 1.1.34  Added my own scaleImg function and fix to label montage
# 2014-12-03  JRM 1.1.35  Added printJavaVersion
# 2014-12-03  JRM 1.1.36  Added makeStackFromListRGB
# 2014-12-03  JRM 1.1.37  Montage functions and dependencies work w/o display
# 2014-12-03  JRM 1.1.38  Added headless capabilities for HueLUT
# 2014-12-12  JRM 1.1.40  Added makeTransparentOverlay
# 2014-12-13  JRM 1.1.41  Added headlessFlatten
# 2014-12-14  JRM 1.1.42  changed vertProfileFromROI to have headless flag
# 2014-12-14  JRM 1.1.43  Added makeStackFromImageFiles for stacks with each slice
#                         with optimum brightness/contrast LUT
# 2014-12-18  JRM 1.1.44  Added  headlessCropStack
#                         TO DO: add error checking
# 2014-12-20  JRM 1.1.45  Added smoothMapImage

import sys
import os
import glob
import shutil
import time
import math
import csv

from colorsys import hsv_to_rgb

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from java.awt import Color
import java.io as jio
import java.lang as jl
import java.util as ju

import jarray

from ij import IJ, ImagePlus, WindowManager, Prefs, ImageStack

from ij.io import FileInfo

from ij.gui import Roi, TextRoi, ImageRoi, Overlay, ImageCanvas, ShapeRoi

from ij.measure import ResultsTable, Calibration, Measurements
from ij.plugin import ImageCalculator, Duplicator, ChannelSplitter
from ij.plugin import MontageMaker
from ij.plugin.frame import RoiManager

from ij.process import LUT, ImageProcessor, StackProcessor

from script.imglib.math import Compute, Divide, Multiply, Subtract  
from script.imglib.algorithm import Gauss, Scale2D, Resample  
from script.imglib import ImgLib 



"""A series of wrapper scripts to make ImageJ Jython automation easy
and to avoid re-writing the same code - The Do not Repeat Yourself (DRY) principle...
Place this file in FIJI_ROOT/jars/Lib/  call with
import jmFijiGen as jmg"""

def smoothMapImage(imp, sat=0.00001):
  """smoothMapImage(imp, sat=0.00001)
  Smooths an X-ray map image (typically a 16 bit gray image) with a 3x3 kernel and
  converts it to an 8 bit gray scale image that spans 0-255. This is ready for a 
  hueLUT. It peforms this on a duplicate imp and returns the resultant imp. To the
  best of my understanding, this is how Oxford treats their maps. 
  Inputs:
  imp - the input ImagePlus object
  sat - the saturation, default 0.00001 to truncate very little from the max
  Returns:
  ret - an ImapePlus for the 8-bit, scaled, filtered image
  """
  ret = imp.duplicate()
  name = imp.getShortTitle()
  ip = ret.getProcessor()
  ip.smooth()
  stats = ret.getStatistics(Measurements.MIN_MAX)
  imp.setDisplayRange(stats.min, stats.max)
  strEC = "saturated=%g" % sat
  IJ.run(ret, "Enhance Contrast", strEC)
  IJ.run(ret, "8-bit", "")
  ret.setTitle(name)
  return ret

def headlessCropStack(imp, lRoi):
  """headlessCropStack(imp, lRoi)
  Crop a stack to a rectangle given by the list, lRoi
  Inputs:
  imp  - the ImagePlus of the stack to crop
  lRoi - a list with [x0, y0, w, h]
  Returns:
  imp - the ImagePlus of the cropped stack
  """
  ip = imp.getProcessor()
  roi = ShapeRoi(Roi(lRoi[0], lRoi[1], lRoi[2], lRoi[3]))
  imp.setRoi(roi)
  stackSize= imp.getStackSize()
  bounds = roi.getBounds()
  newWidth = bounds.width
  newHeight = bounds.height
  interpolationMethod = ImageProcessor.BICUBIC
  ip.setInterpolationMethod(interpolationMethod)
  sp = StackProcessor(imp.getStack(), ip)
  s2 = sp.resize(newWidth, newHeight, False)
  cal = imp.getCalibration()
  cal.xOrigin -= roi.getBounds().x
  cal.yOrigin -= roi.getBounds().y
  imp.setStack(None, s2)
  imp.setCalibration(cal)
  return imp

def makeStackFromImageFiles(lNames, imgDir, stkName='stack', ext='.tif', bUseStackHisto=False):
  """makeStackFromImageFiles(lNames, imgDir, stkName='stack', ext='.tif', bUseStackHisto=False)
  Construct a stack of images from a list of file names
  Inputs:
  lNames         - a list of base file namers
  imgDir         - a path to the image files
  stkName        - the name for the stack (default stack)
  ext            - file extension (default .tif)
  bUseStackHisto - use the same LUT for the whole stack (default False)
  Returns:
  An ImagePlus for the stack"""
  strImg = imgDir + "/" + lNames[0] + ext
  imp = IJ.openImage(strImg)
  newStack = ImageStack(imp.getWidth(), imp.getHeight())
  for name in lNames:
    strImg = imgDir + "/" + name + ext
    imp = IJ.openImage(strImg)
    newStack.addSlice(name, imp.getProcessor())
  ret = ImagePlus(stkName, newStack)
  if bUseStackHisto == True:
    IJ.run(ret, "Enhance Contrast", "saturated=0.35 process_all use")
  else:
    IJ.run(ret, "Enhance Contrast", "saturated=0.35 process_all")
  return ret


def headlessFlatten(imp):
  """headlessFlatten(imp)
  A flatten command that works in headless mode without displaying
  images.
  Inputs:
  imp - The ImagePlus of the image to flatten
  Returns 
  The ImagePlus of the flattened image"""
  flags = imp.isComposite()
  if flags==False:
    IJ.setupDialog(imp, 0)
  ret = imp.flatten()
  ret.setTitle(imp.getShortTitle())
  return ret

def makeFlattenedTransparentOverlay(impBase, impOvr, op=50):
  """makeFlattenedTransparentOverlay(impBase, impOvr, op=50)
  Make a transparent overlay on an image and flattens it. Note:
  this cannot be headless because of the flatten.
  Inputs:
  impBase - the ImagePlus for the underlying image (uses a duplicate)
  impOvr  - the ImagePlus for the image to overlay
  op      - the opacity (default 50%)
  Returns:
  The ImagePlus of the flattened composite image
  """
  imp = impBase.duplicate()
  name = impOvr.getTitle()
  roi = ImageRoi(0, 0, impOvr.getProcessor())
  roi.setOpacity(op/100.0)
  imp.setRoi(roi)
  imp = headlessFlatten(imp)
  # imp.flatten()
  # IJ.run(imp, "Flatten", "")
  # imp.close()
  # imp = IJ.getImage()
  imp.setTitle(impOvr.getShortTitle() + "-ROI" )
  return imp

def makeStackFromListRGB(lImps, strName="Stack"):
  """makeStackFromListRGB(lImps, strName="Stack")
  make a RGB stack from a list of RGB images
  Inputs:
  lImps - a list of ImagePlus from RGB images to create the stack
  strName - a name for the stack. Defaults to Stack
  Returns:
  ImagePlus of the stack
  """
    
  w = lImps[0].getWidth()
  h =  lImps[0].getHeight()
  cal = lImps[0].getCalibration()
  stack = ImageStack(w,h)
  l = len(lImps)
  if l < 2:
    IJ.log("Too few images (%d) passed to makeStackFromListRGB" % l)
    return None
  fi = lImps[0].getOriginalFileInfo()
  if fi == None:
    fi = lImps[l-1].getOriginalFileInfo()
  for i in range(l):
    stack.addSlice(lImps[i].getShortTitle(), lImps[i].getProcessor().convertToRGB())
  stack.update(lImps[0].getProcessor())
  impStack = ImagePlus(strName, stack)
  impStack.setCalibration(cal)
  fi.fileName = ""
  fi.nImages = impStack.getStackSize()
  impStack.setFileInfo(fi) 
  return impStack

def printJavaVersion():
  """check and print the Java version. Useful to test the effectiveness of supplying
  the JAVA_HOME environment variable in a script."""
  ans="bad"
  if IJ.isJava16():
    ans = "Java 1.6"
    if IJ.isJava17():
      ans = "Java 1.7"
      if IJ.isJava18():
        ans = "Java 1.8"
  print ans        

def scaleImg(imp,factor):
  """scaleImg(imp,factor)
  Scale an input ImagePlus for an image by factor using bicubic interpolation. Returns an ImagePlus"""
  name = imp.getShortTitle()
  averageWhenDownsizing = True
  im = ImageProcessor.BICUBIC
  newWidth = int(round(factor*imp.getWidth(), 0))
  newHeight = int(round(factor*imp.getHeight(), 0))
  ip = imp.getProcessor()
  ip.setBackgroundValue(0)
  imp2 = imp.createImagePlus()
  imp2.setProcessor(name, ip.resize(newWidth, newHeight, averageWhenDownsizing))
  cal = imp2.getCalibration()
  cal.pixelWidth *= 1.0/factor
  cal.pixelHeight *= 1.0/factor  
  return imp2


def labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24, col=Color.WHITE, bHeadless=False):
  """labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24, col=Color.WHITE, bHeadless=False)
  Label a montage in the overlay
  Inputs:
  imp       - the ImagePlus of the montage to label
  lLabels   - a list of labels to write into the overlay
  cols      - the number of columns in the montage
  rows      - the number of rows in the montage
  w0        - the x offset for the label (defaults to 12 px)
  h0        - the y offset for the label (defaults to  2 px)
  font      - the size of the font (pts, defaults to 24)
  col       - color of text. Default to Color.WHITE
  bHeadless - a flag (default False) to suppress display for headless mode
  Returns
  an ImagePlus with a labeled, duplicate of the input image
  """
  # print(cols,rows)
  wBase = imp.getWidth()/cols
  hBase = imp.getHeight()/rows
  # print(wBase, hBase)
  l = len(lLabels)
  xt = 0
  y = 0
  # make a copy
  res = imp.duplicate()
  # let's create an array of text rois
  # first a dummy text ROI to set the font
  tr = TextRoi(10, 10, "Foo")
  tr.setColor(col)
  tr.setFont("SanSerif", font, 1) 
  tr.setJustification(TextRoi.CENTER)
  tr.setAntialiased(True)
  # explicitly save preferences
  Prefs.savePreferences()
  
  ol = Overlay()
  for i in range(l):
    x = (i % cols+1)-1
    if x < xt:
      y += 1
    xt = x
    xL = x * wBase + w0
    yL = y * hBase + h0
    # print(xL,yL)
    tr = TextRoi(xL, yL, lLabels[i])
    tr.setColor(col)
    tr.setFont("SanSerif", font, 1) 
    tr.setJustification(TextRoi.CENTER)
    tr.setAntialiased(True)
    ol.add(tr)
  if bHeadless:
    res.setOverlay(ol)
  else:
    res.setOverlay(ol)
    res.show()
  return res
  
 
def RGBtoMontage(imp, font=24, col=Color.WHITE, bClose=True, bHeadless=False):
  """RGBtoMontage(imp, font=24, col=Color.WHITE, bClose=True, bHeadless=False)
  Split an RGB image into channels, convert each to RGB, and then make a montage of the
  four images.
  Inputs:
  imp       - the ImagePlus of the montage to label
  font      - the size of the font (pts, defaults to 24)
  col       - color of text. Default to Color.WHITE
  bClose    - a flag (default True) 
  bHeadless - a flag (default False) to suppress display for headless mode
  Returns
  an ImagePlus with a labeled, duplicate of the input image
  """
  if bHeadless != True:
    imp.show()
  w = imp.getWidth()
  print(w)
  name = imp.getShortTitle()
  cs = ChannelSplitter()
  [rImg, gImg, bImg] = cs.split(imp)
  if bHeadless != True:
    imp.hide()
  
  rImg.setTitle("R")
  IJ.run(rImg, "RGB Color","")
  if bHeadless != True:
    rImg.show()
    rImg.updateAndRepaintWindow()
  
  gImg.setTitle("G")
  IJ.run(gImg, "RGB Color","")
  if bHeadless != True:
    gImg.show()
    gImg.updateAndRepaintWindow()
  
  bImg.setTitle("B")
  IJ.run(bImg, "RGB Color","")
  if bHeadless != True:
    bImg.show()
    bImg.updateAndRepaintWindow()
  
  lImps = [rImg, gImg, bImg, imp]
  impStack = makeStackFromListRGB(lImps, strName="Stack")
  
  if bHeadless != True:
    impStack.show()
    
  mont = MontageMaker()
  # starts with a stack (stack) and returns an imp to the montage
  # makeMontage2(ImagePlus imp, int columns, int rows, double scale, int first, int last, int inc, int borderWidth, boolean labels) 
  impMont = mont.makeMontage2(impStack, 4, 1, 1.0, 1, 4, 1, 0, False)
 
  # strMon = "columns=4 rows=1 scale=1 first=1 last=4 increment=1 border=0 font=12"
  # IJ.run(impStack, "Make Montage...", strMon)

  # res = IJ.getImage()
  if bClose:
    imp.changes=False
    imp.close()
    if bHeadless != True:
      impStack.changes=False
      impStack.close()

  trR = TextRoi(    10, 0, "R")
  trR.setColor(col)
  trR.setFont("SanSerif", font, 1) 
  trR.setJustification(TextRoi.CENTER)
  trR.setAntialiased(True)
  
  trG = TextRoi(  w+10, 0, "G")
  trG.setColor(col)
  trG.setFont("SanSerif", font, 1) 
  trG.setJustification(TextRoi.CENTER)
  trG.setAntialiased(True)
  
  trB = TextRoi(2*w+10, 0, "B")
  trB.setColor(col)
  trB.setFont("SanSerif", font, 1) 
  trB.setJustification(TextRoi.CENTER)
  trB.setAntialiased(True)

  ol = Overlay()
  ol.add(trR)
  ol.add(trG)
  ol.add(trB)
  impMont.setOverlay(ol)
  if bHeadless != True:
    impMont.updateAndRepaintWindow()
  return impMont
  


def findI0(imp, maxSearchFrac=0.5, chAvg=5):
  """findI0(imp, maxSearchFrac=0.5, chAvg=5)
  search a single channel image from the maximum gray level down to find
  the mean intensity.
  Input parameters:
  imp - the Image Plus
  maxSearchFrac - the maximum fraction of gray space to search, defualt is 0.5
  chAvg         - number of channels on either side of the maximum to average
                  to find the centroid. Defaults to 5
  Returns:
    The mean intensity of the peak or None if there is an error."""
  if imp.getNChannels() > 1:
    IJ.error("findI0 requires a single channel image")
    return None
  if imp.getNSlices() > 1:
    IJ.error("findI0 requires a single channel image")
    return None
  # need to find max Gray for search. 16 bit images have a lot of empty cells...
  stats = imp.getStatistics()
  maxGray = int(stats.max)
  minGray = int(maxSearchFrac*stats.max)
  delta = maxGray - minGray
  ipHis = imp.getProcessor().getHistogram()
  iMax = iPk = 0
  for x in range(delta):
    i = maxGray-x-1
    if(ipHis[i] > iPk):
      iPk = ipHis[i]
      iMax = i
  sumI = 0
  sumH = 0
  for x in range(2*chAvg+1):
    i = iMax - chAvg + x
    sumI += i * ipHis[i]
    sumH += ipHis[i]  
  iZero = float(sumI) / float(sumH)
  return (iZero)



def isNaN(num):
  """isNaN(num)
  Check if a number is NaN, returning True of False"""
  return num != num

def checkNaN(x):
  """checkNaN(x)
  This checks if a value (e.g. K-ratio) is NaN and sets the value to
  zero if it is. This really helps when writing data frames to be
  read by R."""
  if isNaN(x):
    x = 0.0
  return x
  

def i2b(i):
  """def i2b(i)
  Convert an integer to a byte. Useful for LUTs."""
  if i > 127:
    i -= 256
  if i < -128:
    i = 128
  return i

def burnBox(imp, lRoi, col="green", wid=2):
  """burnBox(imp, lRoi, col="green", wid=2)
  Burn a box into an ImagePlus
  Input parameters
  imp  - the ImagePlus
  lRoi - a list with [x0,y0,w,h]
  col  - the color, default is green
  wid  - the line width default = 3"""
  roi = Roi(lRoi[0], lRoi[1], lRoi[2], lRoi[3])
  imp.setRoi(roi)
  strStroke = "  stroke=%s width=%g" % (col, wid)
  IJ.run(imp, "Properties... ", strStroke )
  IJ.run(imp, "Add Selection...", "")

def hueDegToRGBCol(hue):
  """hueDegToRGBCol(hue)
  Convert a hue balue (0 to 360 degrees) to an RGB color.
  Useful for LUTs."""
  h = hue / 360.
  [r, g, b] =  hsv_to_rgb(h, 1.0, 1.0)
  ret = [255.0*r, 255.0*g, 255.0*b]
  return ret
  
def applyHueLUT(imp, hueDeg, gamma=1.0, bHeadless=False):
  """applyHueLUT(imp, hueDeg, gamma=1.0, bHeadless=False))
  Create and a apply a LUT to an ImagePlus where the maximum intensity corresponds to
  the hue specified by hueDeg. Optionally apply a gamma.
  Input Parameters
  imp - the ImagePlus
  hueDeg - the hue angle, in degrees, from 0 to 360
  gamma  - an optional gamma correction, defaults to 1.0
  bHeadless - an optional flag, default False, that when true supresses display for headless mode
  Returns
  an ImagePlus with the new LUT applied"""
  ret = imp.duplicate()
  r, g, b = hueDegToRGBCol(hueDeg)
  print(r,g,b)
  ra = jarray.zeros(256, 'b')
  ga = jarray.zeros(256, 'b')
  ba = jarray.zeros(256, 'b')

  
  for i in range(256):
    ra[i] = i2b(int(round(r*pow(float(i)/256., gamma))))
    ga[i] = i2b(int(round(g*pow(float(i)/256., gamma))))
    ba[i] = i2b(int(round(b*pow(float(i)/256., gamma))))

  lut = LUT(ra, ga, ba)
  ip = ret.getProcessor() 
  ip.setLut(lut)
  if bHeadless != True:
    ret.updateImage() 
  
  return ret


def getUnitString(units=-6):
  """getUnitString(units)
  Get a unit string given a power w.r.t. meters
  Input:
  units - an integer defaults to -6 for microns
  Return
  A string"""
  if(units == -6):
    a = [0xC2, 0xB5]
    mu = "".join([chr(c) for c in a]).decode('UTF-8')
    scaUni  = mu+"m"
  if(units == -3):
    scaUni  = "mm"
  if(units == -9):
    scaUni  = "nm"
  if(units == 0):
    scaUni  = "m"
  if(units == 3):
    scaUni  = "km"
  return(scaUni)


def vertProfileFromROI(imp, lRoi, sFact, bHeadless=True):
  """vertProfileFromROI(imp, lRoi, sFact, bHeadless=True)
  Generate an averaged vertical profile from a rectangular ROI from an
  ImagePlus
  Inputs:
  imp       - the ImagePlus
  lRoi      - a list with the parameters to construct the ROI
  sFact     - a scale factor, defaults to 1 for pixels.
  bHeadless - a flag (default True) to supress display for headless operation
  Returns
  a list with two arrays, distance and intensity"""
  if (len(lRoi) != 4):
    IJ.error("Not a proper rectangle","This function expects a 4 item list for the ROI")
    return None
  if bHeadless == False:
    imp.show()
  cal = imp.getCalibration()
  impROI = imp.duplicate()
  impROI.setCalibration(cal)
  impROI.setRoi(lRoi[0],lRoi[1],lRoi[2],lRoi[3])
  IJ.run(impROI,"Crop","")
  if bHeadless == False:
    imp.close()
    impROI.show()
  w = impROI.getWidth()
  h = impROI.getHeight()
  ip = impROI.getProcessor()
  ar = ip.getPixels()  
  x = []
  y = []
  for j in xrange(h):
    x.append(round(sFact*j, 3))
    gSum = 0.
    for i in xrange(w):
      gSum += float(ar[j*w+i])
    gAvg = gSum / float(w)
    y.append(round(gAvg, 1))
  ret = [x,y]
  if bHeadless == False:
    impROI.changes = False
    impROI.close()
  return ret


def procAZtecTifMap(imp, colStr, gamma=1.0, theta=5):
  """procAZtecTifMap(imp, colStr, gamma=1.0, theta=5)
  Process an ImagePlus from an AZtec X-ray map exported as a TIF
  Inputs:
  imp    - the ImagePlus
  colStr - a color string for the LUT
  gamma  - a gamma transform for the map. defaults to 1
  theta  - parameter for ROF denoising. default = 5.
  Returns:
  An ImagePlus for the transformed image  
  """
  # start with a copy
  name = imp.getShortTitle()
  impRet = imp.duplicate()
  # impRet.show()
  ip = impRet.getProcessor()
  theMax = ip.getMax()
  IJ.run(impRet, "32-bit","")
  IJ.run(impRet, "ROF Denoise", "theta=%g" % theta)
  IJ.setMinAndMax(impRet, 0, theMax);
  IJ.run(impRet, "8-bit", "")
  IJ.run(impRet,"Gamma...", "value=%g" % gamma)
  IJ.run(impRet, colStr, "")
  IJ.run(impRet, "RGB Color", "")
  impRet.setTitle(name + "-pr")
  # impRet.updateAndRepaintWindow()
  return impRet
  
def calStackZ(imp, scaleX, scaleY, scaleZ, units=-6, bVerbose=False):
  """calStackZ(imp, scaleX, scaleY, scaleZ, units=-6,  bVerbose=False)
  Calibrate a stack from it's ImagePlus and scale factors
  Inputs
  imp - the ImagePlus
  scaleX - the scale factor for the width
  scaleY - the scale factor for the height
  scaleZ - the scale factor for the depth
  unit   - the power for the units w.r.t. meters defaults to -6 (microns)
  Returns - the ImagePlus of the calibrated stack
  """
  nS = imp.getNSlices()
  if(nS < 2):
    IJ.error("Not a stack","This function expects a Z-stack")
    return None
  cal = imp.getCalibration()
  
  
  zO = 0.5*(nS-1)
  cal.zOrigin = zO
  
  scaUni = getUnitString(units)
  cal.setUnit(scaUni)
  cal.pixelWidth  = scaleX
  cal.pixelHeight = scaleY
  cal.pixelDepth  = scaleZ
  imp.setCalibration(cal)
  
  # imp.updateAndRepaintWindow() 

  if(bVerbose):
    print(nS)
    print(cal)
  
  return imp

def whiteBalance(imp, bVerbose=False):
  """whiteBalance(imp, bVerbose=False)
  White balance an image from a ROI. Requires a ROI of the neutral area.
  Adapted from the macro by  Vytas Bindokas; Oct 2006, Univ. of Chicago
  Input parameters
  imp - the input ImagePlus
  bVerbose - a boolean, default False, whether to print info
  Returns
  An ImagePlus of the corrected image (displayed)"""
  if(imp==None):
    IJ.error("Missing Image","you must have an image with a region first")
    return None
  name = imp.getShortTitle()
  w = imp.getWidth()
  h = imp.getHeight()
  wbROI = imp.getRoi()
  if (wbROI==None):
    IJ.error("Missing ROI","you must draw region first")
    return None
  IJ.run("RGB Stack")
  # work = WindowManager.getCurrentImage()
  IJ.run("Set Measurements...", "mean redirect=None decimal=3")
  rm = RoiManager()
  rm.select(imp, 0)
  imp.setSlice(1)
  IJ.run("Measure")
  imp.setSlice(2)
  IJ.run("Measure")
  imp.setSlice(3)
  IJ.run("Measure")
  rt = ResultsTable.getResultsTable()
  mc = rt.getColumnIndex("Mean")
  ct = rt.getCounter()
  r = rt.getValueAsDouble(mc, 0)
  g = rt.getValueAsDouble(mc, 1)
  b = rt.getValueAsDouble(mc, 2)
  t=((r+g+b)/3)
  dR=r-t
  dG=g-t
  dB=b-t
  # val = rt.getValueAsDouble(0, 0)
  if(bVerbose==True):
    print(name)
    print("ROI:")
    print(wbROI)
    print("Mean R,G,B")
    print(r,g,b)
    print("Mean dR,dG,dB")
    print(dR,dG,dB)
  # R=getResult("Mean")
  # print(R)
  IJ.makeRectangle(0, 0, w, h)
  IJ.run("16-bit")
  IJ.run("32-bit")
  imp.setSlice(1)
  strSlice = "slice value=%f" % abs(dR)
  if (dR<0):
    IJ.run("Add...", strSlice )
  if (dR>0):
    IJ.run("Subtract...", strSlice)
  
  imp.setSlice(2)
  strSlice = "slice value=%f" % abs(dG)
  if (dG<0):
    IJ.run("Add...",  strSlice )
  if (dG>0):
    IJ.run("Subtract...",  strSlice )

  strSlice = "slice value=%f" % abs(dB)
  imp.setSlice(3)
  if (dB<0):
    IJ.run("Add...", strSlice )
  if (dB>0):
    IJ.run("Subtract...", strSlice )
    
  rm.runCommand("Deselect")
  IJ.run("16-bit")
  work = WindowManager.getCurrentImage()
  IJ.run("Convert Stack to RGB")
  imp = WindowManager.getCurrentImage()
  imp.show()
  work.changes = False
  work.close()
  work.flush() # clean up memory...
  IJ.selectWindow("ROI Manager")
  IJ.run("Close");
  IJ.selectWindow("Results")
  IJ.run("Close")
  imp.setTitle(name + "-wb")
  imp.updateAndDraw()
  return imp


def computeStats(lis):
  """computeStats(lis)
  Compute key statistics for a 1-d array (list)
  Input:
  lis - a 1-d vector (list)
  Returns:
  [mu, sd, count] as a vector"""
  count = len(lis)
  mu = sum(lis) / float(count)
  s = 0
  for i in range(count):
    s += pow(lis[i] - mu, 2)
  sd = math.sqrt(s / float(count -1))
  res = [mu, sd, count]
  return res
  

def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)
    
def makeTmpDir():
  """makeTmpDir()
  Make a working directory in $IMG_ROOT and make sure it is clean."""
  imgDir  = os.environ['IMG_ROOT']
  tmpDir = imgDir + "/tmp"
  ensureDir(tmpDir)
  strPath = tmpDir + "/*.*"
  files = glob.glob(strPath)
  for file in files:
    os.unlink(file)
  return tmpDir
  
def makeMontage(lNames, columns, rows, inDir, inExt= ".png", sca=1.0, lCal=[], lCr=None, bDebug=False, bHeadless=False):
  """makeMontage(lNames, columns, rows, inDir, inExt= ".png", sca=1.0, lCal=[], lCr=None, bDebug=False, bHeadless=False)
  Make a montage from a list of file names
  Parameters:
  lNames    - a list of file names
  columns   - number of columns in the montage
  rows      - number of rows in the montage
  inDir     - input directory for images
  inExt     - input extension for images - default = .png
  sca       - scale factor, default = 1.0
  lCal      - an optional list of calibration info: [fullWidth, baseImgWidthPx, -6]
  lCr       - an optional list of parameters for a crop [x0,y0,w, h], default is None
  bDebug    - a flag, default = False, to print diagnostic info
  bHeadless - a flag, default = False, to suppress display for headless mode
  Returns
  The ImagePlus corresponding to the montage"""
  lImp = []
  l = len(lNames)
  l2 = len(lCal)
  IJ.run("Close All")
  for i in range(l):
    if bDebug:
      print(lNames[i])
    inImg = inDir + "/" + lNames[i] + inExt
    if bDebug:
      print(inImg)
    raw = IJ.openImage(inImg)
    lImp.append(raw)
    if bHeadless == False:
      raw.show()
  impStack = makeStackFromListRGB(lImp)
  for imp in lImp:
    imp.close()
  if(lCr != None):
    headlessCropStack(impStack, lCr)
    # IJ.makeRectangle(lCr[0], lCr[1], lCr[2], lCr[3])
    # IJ.run(impStack, "Crop", "")
  
  mont = MontageMaker()
  # starts with a stack (stack) and returns an imp to the montage
  # makeMontage2(ImagePlus imp, int columns, int rows, double scale, int first, int last, int inc, int borderWidth, boolean labels) 
  impMont = mont.makeMontage2(impStack, columns, rows, sca, 1, l, 1, 0, False)
  # strMon = "columns=%g rows=%g scale=%f first=1 last=%d increment=1 border=0 font=12" % (columns, rows, sca, l)
  # IJ.run("Make Montage...", strMon)
  if (bDebug==False):
    impStack.changes = False
    impStack.close()
  if (l2 == 3):
      impMont = calibAZtecImage(impMont, lCal[0], lCal[1], units=lCal[2])
  return impMont
  
def calibImage(theImp, fullWidth, units=-6):
  """calibImage(theImp, fullWidth, units=-6)
  Calibrate the ImagePlus
  Inputs
  theImp    - the ImagePlus to calibrate
  fullWidth - the full width of the image, typically in microns
  units     - the exponent w.r.t. meters. Defaults to -6 (microns)
  Returns   - the ImagePlus of the calibrated image"""
  scaUni = getUnitString(units)
  w = float(theImp.getWidth())
  sf = fullWidth/w
  cal = theImp.getCalibration()
  cal.setXUnit(scaUni)
  cal.setYUnit(scaUni)
  cal.pixelWidth  = sf
  cal.pixelHeight = sf
  theImp.setCalibration(cal)
  # s1 = "distance=%d known=%f unit=%s" % (w, fullWidth, scaUni)
  # IJ.run(theImp, "Set Scale...", s1)
  return theImp

def calibImageDirect(theImp, unPerPx, units=-6):
  """calibImage(theImp, unPerPx, units=-6)
  Directly calibrate the ImagePlus
  Inputs
  theImp  - the ImagePlus to calibrate
  unPerPx - the spacing between pixels in units
  units   - the exponent w.r.t. meters. Defaults to -6 (microns)
  Returns - the ImagePlus of the calibrated image"""
  scaUni = getUnitString(units)
  cal = theImp.getCalibration()
  cal.setXUnit(scaUni)
  cal.setYUnit(scaUni)
  cal.pixelWidth  = unPerPx
  cal.pixelHeight = unPerPx
  # theImp.setCalibration(cal)
  # w = theImp.getWidth()
  # s1 = "distance=1 known=%f unit=%s" % (unPerPx, scaUni)
  # IJ.run(theImp, "Set Scale...", s1)
  return theImp

def calibAZtecImage(theImp, fullWidth, baseImgWidth, units=-6):
  """calibAZtecImage(theImp, fullWidth, baseImgWidth, units=-6)
  Calibrate the ImagePlus using the AZtec convention of a full
  width in sample space and a base image width. This lets one
  calibrate montages from uncalibrated png images...
  Inputs
  theImp       - the ImagePlus to calibrate
  fullWidth    - the full width of the image, typically in microns
  baseImgWidth -  the width, in px, of the base image
  units        - the exponent w.r.t. meters. Defaults to -6 (microns)
  Returns      - the ImagePlus of the calibrated image"""
  scaUni = getUnitString(units)
  w = float(baseImgWidth)
  sf = fullWidth/w
  cal = theImp.getCalibration()
  cal.setXUnit(scaUni)
  cal.setYUnit(scaUni)
  cal.pixelWidth  = sf
  cal.pixelHeight = sf
  theImp.setCalibration(cal)
  # s1 = "distance=%d known=%f unit=%s" % (baseImgWidth, fullWidth, scaUni)
  # IJ.run("Set Scale...", s1)
  return theImp

def doCrop(theImp, lPar):
  """doCrop(theImp, lPar)
  Crop an ImagePlus to a rectangle with the parameter list, lPar
  lPar = [x0,y0,width,height]
  returns an ImagePlus with the cropped image."""
  if (len(lPar) != 4):
    IJ.log("You need to pass a list of 4 integers [x,y,w,h] to doCrop")
    return None      
  name = theImp.getShortTitle() + "-cr"
  cal = theImp.getCalibration()
  # make a copy
  imp = theImp.duplicate()
  imp.setCalibration(cal)
  w = imp.getWidth()
  h = imp.getHeight()
  imp.setRoi(lPar[0],lPar[1],lPar[2],lPar[3])
  IJ.run(imp,"Crop","")
  imp.setTitle(name)
  return (imp)
  
def makeTiles(inpDir, outDir, lNames, inExt='.png', cropPar=None, bDebug=False):
  """makeTiles(inDir, outDir, lNames, inExt='.png', cropPar=None, bDebug=False)
  Construct tile-#.tif files from a list of file names with default extension
  png, cropping if a list is supplied.
  This function is deprecated. Use makeMontage instead
  Input parameters:
  inpDir  - input directory (with / separators, no terminating)
  outDir  - output directory ...
  lNames  - a list of file names
  iExt    - input file extension (default '.png') 
  cropPar - a list [x0,y0,width,height] default = None
  bDebug  - print debugging messages, default False"""
  l = len(lNames)
  for i in range(l):
    if bDebug:
      print(lNames[i])
    inImg = inpDir + "/" + lNames[i] + inExt
    if bDebug:
      print(inImg)
    raw = IJ.openImage(inImg)
    # raw.show()
    if (cropPar==None):
      cr = raw
    else:
      cr = doCrop(raw, cropPar)
    cr.show()
    ensureDir(outDir)
    outImg = "%s/tile-%g.tif" % (outDir, i+1)
    if bDebug:
      print(outImg)
    IJ.saveAsTiff(cr, outImg)
    cr.close()

def makeStackFromDir(inpDir, inExt='.tif', bDebug=False):
  """makeStackFromDir(inpDir, inExt='.tif', bDebug=False)
  Make a stack from all files in a directory
  """
  for file in os.listdir(inpDir):
    if file.endswith(inExt):
      path = inpDir + "/" + file
      raw = IJ.openImage(path)
      raw.show()
  IJ.run("Images to Stack")
  impStack = WindowManager.getCurrentImage()
  return impStack


def stitchMaps(tifDir, cols, rows):
  """stitchMaps(tifDir, cols, rows)
  stitch images from an Oxford Map
  This function is deprecated. Use makeMontage instead
  Input Parameters:
  tifDir - directory with tif files
  cols   - number of columns ... e.g. 2
  rows   - number of rows ...... e.g. 3
  Returns:
  imp     - an ImagePlus
  """
  s1  = "Grid/Collection stitching"
  s2a = "type=[Grid: column-by-column] order=[Down & Right                ] "
  s2b = "grid_size_x=%g grid_size_y=%g tile_overlap=0 first_file_index_i=1 directory=%s" % (cols, rows, tifDir)
  s2c = " file_names=tile-{i}.tif output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] "
  s2d = "regression_threshold=0.30 max/avg_displacement_threshold=2.50 "
  s2e = "absolute_displacement_threshold=3.50 computation_parameters=[Save memory (but be slower)] "
  s2f = "image_output=[Fuse and display] use"
  
  s2 = s2a + s2b +s2c + s2d +s2e + s2f
  # print(s2)
  IJ.run(s1, s2)
  imp = WindowManager.getCurrentImage()
  IJ.run("RGB Color")
  imp.close()
  imp = WindowManager.getCurrentImage()
  return imp
  
def addScaleBar(theImp, scaFac, scaUni, barWid, barHt, barFnt, barCol, barLoc):
  """addScaleBar(theImp, scaFac, scaUni, barWid, barHt, barFnt, barCol, barLoc)
  Add a scale bar to an image 
  Input Parameters:
  theImp - the ImagePlus of the input image
  scaFac - scale factor ........ e.g. 1.2
  scaUni - scale units ......... e.g. "nm"
  barWid - bar width (units) ... e.g. 100
  barHt  - bar ht px ........... e.g. 9
  barFnt - bar font ............ e.g. 48
  barCol - bar color ........... e.g. "White"
  barLoc - bar location ........ e.g. "Lower Right"
  """
  theImp.show()
  foo = theImp.duplicate()
  s1 = "distance=1 known=%f unit=%s" % (scaFac, scaUni)
  IJ.run(theImp, "Set Scale...", s1)
  s2 = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barWid, barHt, barFnt, barCol, barLoc)
  # dummy to get things set
  IJ.run(foo, "Add Scale Bar", s2)
  # explicitly save preferences
  Prefs.savePreferences()
  foo.changes = False
  foo.close()
  IJ.run(theImp, "Add Scale Bar", s2) 
  
def flatFieldCorrectRGB(impImg, impFF, sigma=100):
  """flatFieldCorrectRGB(impImg, impFF, sigma=100)
  Do a flat-field (shading) correction for an RGB image
  Input Parameters:
  impImg - The image plus for an RGB image to correct for shading
  impFF  - An even illumination image (gain) 
  sigma  - blur parameter for a Gaussian blur for the gain image. default = 100 (px)
  Returns an ImagePlus for the corrected image which is displayed
  TO DO: error checking
  """
  strSigma = "sigma=%g" % sigma
  name = impImg.getShortTitle()
  cs = ChannelSplitter()
  impImg.show()
  [rImg, gImg, bImg] = cs.split(impImg)
  impImg.changes = False
  impImg.close()
  impImg.flush() # clean up memory...
  rImg.setProcessor(rImg.getProcessor().convertToFloat()) 
  gImg.setProcessor(gImg.getProcessor().convertToFloat()) 
  bImg.setProcessor(bImg.getProcessor().convertToFloat()) 

  impFF.show()
  [rBkg, gBkg, bBkg] = cs.split(impFF)
  impFF.changes = False
  impFF.close()
  impFF.flush() # clean up memory...
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
  impComp.flush() # clean up memory...

  impSc = WindowManager.getCurrentImage()
  impSc.setTitle(name + "-sc")
  impSc.updateAndDraw()

  return impSc
  
def smoothFlatField(theImp, scaFac=0.25, bShowIntermediate=False):
  """smoothFlatField(theImp, scaFac=0.25, bShowIntermediate=False)
  Smooth a flat field correction image to generate a gain reference image.
  Uses ideas from: http://www.ini.uzh.ch/~acardona/fiji-tutorial/
  Input Parameters:
  theImp - the ImagePlus of the input image
  scaFac - scale factor ... default = 0.25
  bShowIntermediate - show work ... default = False
  Return:
  an ImagePlus with the flat field corrected image
  """
  # 1. wrap the ImagePlus to an ImgLib1 image
  name = theImp.getShortTitle()
  
  img = ImgLib.wrap(theImp)
  if bShowIntermediate:
    # theImp.setTitle("raw")
    theImp.show()
    
  
  # 2. Simulate a gain image from a Gauss with a large radius  
  # (First scale down by 1/scalefac X, then gauss of radius=20, then scale up)  
  # Faster than a big median filter
  gain = Resample(Gauss(Scale2D(img, scaFac), 20), img.getDimensions())
  impGain = ImgLib.wrap(gain)
  impGain.setTitle(name + "-sm")
  return impGain
  
  

def flatField(theImp, scaFac=0.25, bShowIntermediate=False):
  """flatField(theImp, scaFac=0.25, bShowIntermediate=False)
  Do a flat field correction by generating a gain reference image.
  Uses ideas from: http://www.ini.uzh.ch/~acardona/fiji-tutorial/
  Input Parameters:
  theImp - the ImagePlus of the input image
  scaFac - scale factor ... default = 0.25
  bShowIntermediate - show work ... default = False
  Return:
  an ImagePlus with the flat field corrected image
  """
  # 1. wrap the ImagePlus to an ImgLib1 image
  img = ImgLib.wrap(theImp)
  if bShowIntermediate:
    # theImp.setTitle("raw")
    theImp.show()
    
  
  # 2. Simulate a gain image from a Gauss with a large radius  
  # (First scale down by 1/scalefac X, then gauss of radius=20, then scale up)  
  # Faster than a big median filter
  gain = Resample(Gauss(Scale2D(img, scaFac), 20), img.getDimensions())  
  
  # 3. Simulate a perfect dark current  
  darkcurrent = 0  
  
  # 4. Compute the mean pixel intensity value of the image  
  mean = reduce(lambda s, t: s + t.get(), img, 0) / img.size()  

  impGain = ImgLib.wrap(gain)
  if bShowIntermediate:
    impGain.setTitle("gain")
    impGain.show()
    IJ.run("Enhance Contrast", "saturated=0.35") 
  
  # 5. Correct the illumination  
  corrected = Compute.inFloats(Multiply(Divide(Subtract(img, gain),  
                                               Subtract(gain, darkcurrent)), mean))  
  
  # 6. ... and show it in ImageJ  
  impCor = ImgLib.wrap(corrected)
  impCor.setTitle(theImp.getTitle() + "-sc")
  impCor.show()
  IJ.run("Enhance Contrast", "saturated=0.35")
  return impCor

def median(imp, radius):
  """ Apply a median filter to a copy
      of the given ImagePlus, and return it.
      from: http://fiji.sc/Jython_Scripting"""
  copy = Duplicator().run(imp)
  IJ.run(copy, "Median...", "radius=" + str(radius))
  return copy
 
def removeOutliers(imp, radius, threshold, bright):
  """ Apply a remove outliers filter to a copy
      of the given ImagePlus, and return it.
      from: http://fiji.sc/Jython_Scripting"""
  copy = Duplicator().run(imp)
  which = "Bright" if bright else "Dark"
  IJ.run(copy, "Remove Outliers...", "radius=" + str(radius) \
      + " threshold=" + str(threshold) + " which=" + which)
  return copy