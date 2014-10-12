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


import sys
import os
import glob
import shutil
import time
import math
import csv
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import java.io as jio
import java.lang as jl
import java.util as ju

from ij import IJ
from ij import ImagePlus
from ij import WindowManager

from ij.plugin import Duplicator

from script.imglib.math import Compute, Divide, Multiply, Subtract  
from script.imglib.algorithm import Gauss, Scale2D, Resample  
from script.imglib import ImgLib 



"""A series of wrapper scripts to make ImageJ Jython automation easy
and to avoid re-writing the same code - The Do not Repeat Yourself (DRY) principle...
Place this file in FIJI_ROOT/jars/Lib/  call with
import jmFijiGen as jmg"""


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
  
def makeMontage(lNames, columns, rows, inDir, inExt= ".png", sca=1.0, lCal=[], lCr=None, bDebug=False):
  """makeMontage(lNames, columns, rows, inDir, inExt= ".png", sca=1.0, lCal=[], lCr=None, bDebug=False)
  Make a montage from a list of file names
  Parameters:
  lNames  - a list of file names
  columns - number of columns in the montage
  rows    - number of rows in the montage
  inDir   - input directory for images
  inExt   - input extension for images - default = .png
  sca     - scale factor, default = 1.0
  lCal    - an optional list of calibration info: [fullWidth, baseImgWidthPx, -6]
  lCr     - an optional list of parameters for a crop [x0,y0,w, h], default is None
  bDebug  - a flag, default = False, to print diagnostic info"""
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
    raw.show()
  IJ.run("Images to Stack")
  impSeq = WindowManager.getCurrentImage()
  if(lCr != None):
    IJ.makeRectangle(lCr[0], lCr[1], lCr[2], lCr[3])
    IJ.run("Crop")
    impSeq = WindowManager.getCurrentImage()
  strMon = "columns=%g rows=%g scale=%f first=1 last=%d increment=1 border=0 font=12" % (columns, rows, sca, l)
  IJ.run("Make Montage...", strMon)
  if (bDebug==False):
    impSeq.changes = False
    impSeq.close()
  imp = WindowManager.getCurrentImage()
  if (l2 == 3):
      imp = calibAZtecImage(imp, lCal[0], lCal[1], units=lCal[2])
  return imp
  
def calibImage(theImp, fullWidth, units=-6):
  """calibImage(theImp, fullWidth, units=-6)
  Calibrate the ImagePlus
  Inputs
  theImp    - the ImagePlus to calibrate
  fullWidth - the full width of the image, typically in microns
  units     - the exponent w.r.t. meters. Defaults to -6 (microns)
  Returns   - the ImagePlus of the calibrated image"""
  theImp.show()
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
  w = theImp.getWidth()
  s1 = "distance=%d known=%f unit=%s" % (w, fullWidth, scaUni)
  IJ.run("Set Scale...", s1)
  theImp.show()
  return theImp

def calibImageDirect(theImp, unPerPx, units=-6):
  """calibImage(theImp, unPerPx, units=-6)
  Directly calibrate the ImagePlus
  Inputs
  theImp  - the ImagePlus to calibrate
  unPerPx - the spacing between pixels in units
  units   - the exponent w.r.t. meters. Defaults to -6 (microns)
  Returns - the ImagePlus of the calibrated image"""
  theImp.show()
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
  w = theImp.getWidth()
  s1 = "distance=1 known=%f unit=%s" % (unPerPx, scaUni)
  IJ.run("Set Scale...", s1)
  theImp.show()
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
  theImp.show()
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
  s1 = "distance=%d known=%f unit=%s" % (baseImgWidth, fullWidth, scaUni)
  IJ.run("Set Scale...", s1)
  theImp.show()
  return theImp

def doCrop(theImp, lPar):
  """doCrop(theImp, lPar)
  Crop an ImagePlus to a rectangle with the parameter list, lPar
  lPar = [x0,y0,width,height]
  returns an ImagePlus with the cropped image."""
  theImp.show()
  IJ.makeRectangle(lPar[0], lPar[1], lPar[2], lPar[3])
  IJ.run("Crop")
  imp = WindowManager.getCurrentImage()
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
  s1 = "distance=1 known=%f unit=%s" % (scaFac, scaUni)
  IJ.run("Set Scale...", s1)
  s2 = "width=%g height=%g font=%g color=%s location=[%s] bold" % (barWid, barHt, barFnt, barCol, barLoc)
  IJ.run("Add Scale Bar", s2) 

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