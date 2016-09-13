from __future__ import division
# -*- coding: utf-8 -*-
# jmFijiGen.py
# ImageJ Jython - J. R. Minter - 2014-09-11
#
#    Modifications
#    Date     Who   Ver                      What
# ----------  ---  ------  ---------------------------------------------
# 2014-09-11  JRM  1.1.00  First test ensureDir
# 2016-01-21  JRM  1.5.62  Updated anaParticlesWatershed
# 2016-05-02  JRM  1.5.63  Make more PEP8 compliant
# 2016-05-03  JRM  1.5.64  Added functions for circular particles
# 2016-05-03  JRM  1.5.65  Fixed addRoiToOverlay
# 2016-06-10  JRM  1.6.00  Added version info and fixed watershed
# 2016-08-03  JRM  1.6.05  Added measureFeatureLength
# 2016-08-04  JRM  1.6.06  Added measurement counter to 
#                          measureFeatureLength

__revision__ = "$Id: jmFijiGen.py John R. Minter 2014-08-04$"
__version__ = "1.6.06"

import sys
import os
import glob
import shutil
import datetime
import time
import math
import csv

import os, shutil

from math import *
from math import sqrt

from colorsys import hsv_to_rgb

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from java.awt import Color, Font

import java.io as jio
import java.lang as jl
import java.util as ju

import jarray

from ij import IJ, ImagePlus, WindowManager, Prefs, ImageStack

from ij.io import FileInfo, FileOpener,  DirectoryChooser, FileSaver

from ij.gui import Roi, TextRoi, ImageRoi, Overlay, ImageCanvas
from ij.gui import ShapeRoi, PointRoi

from ij.measure import ResultsTable, Calibration, Measurements
from ij.plugin import ImageCalculator, Duplicator, ChannelSplitter
from ij.plugin import MontageMaker
from ij.plugin.filter import ParticleAnalyzer, Analyzer, EDM
from ij.plugin.frame import RoiManager

from ij.process import LUT, ImageProcessor, StackProcessor
from ij.process import ImageStatistics, AutoThresholder
from ij.process.AutoThresholder import getThreshold
from ij.process.AutoThresholder import Method 


from script.imglib.math import Compute, Divide, Multiply, Subtract
from script.imglib.algorithm import Gauss, Scale2D, Resample
from script.imglib import ImgLib 

import mpicbg.imglib.image.ImagePlusAdapter
import mpicbg.imglib.image.display.imagej.ImageJFunctions
import fiji.process.Image_Expression_Parser



"""A series of wrapper scripts to make ImageJ Jython automation easy
and to avoid re-writing the same code - The Do not Repeat Yourself
(DRY) principle...
Place this file in FIJI_ROOT/jars/Lib/    call with
import jmFijiGen as jmg""" 

def measureFeatureLength(imp, lw = 2, csvPath=None, bAppend=True,
                         offset = -30, digits = 3,
                         font = 18, linCol = Color.YELLOW,
                         labCol = Color.WHITE,
                         bDebug = False):
    """
    measureFeatureLength(imp, lw = 2, csvPath=None, bAppend=True,
                         offset = -30, digits = 3,
                         font = 18, linCol = Color.YELLOW,
                         labCol = Color.WHITE,
                         bDebug = False)

    Manually measure the length of a feature in a calibrated ImagePlus
    and write the results to the overlay.

    Version of 2016-08-04

    Parameters
    ----------

    imp: ImagePlus
        The image to process
    lw: int (2)
        The linewidth for the line
    csvPath: string (None)
        The path to a csv file to write measurements
    bAppend: Boolean (True)
        A flag. If True new results are appended to the file 
    offset: int (-30)
        The Y offset for the label. If negative, the label will
        be written above the measurement, if positive below.
    digits: int (3)
        Round the output (in calibrated units) to this number of decimal
        points.
    font: int (18)
        The font size for the measurement.
    linCol: A color constant (Color.YELLOW)
        The color for the line in the overlay.
    labCol: A color constant (Color.WHITE)
        The color for the label
    bDebug: A Boolean (False)
        A flag to print diagnostic incormation

    Returns
    -------
    None - it does draw in the overlay of the image and write an
           optional .csv file.

    Known Issues
    ------------
    With large line widths the length of the drawn line appears lw 
    pixels too long.
    """

    # First define some convenience functions
    def resetLastMeasureCount():
        Prefs.set("JRM.meas.counter", 0)

    def GetLastMeasureCount():
        myCount = Prefs.get("JRM.meas.counter", int(-1))
        if myCount < 0:
            # it was not set, so set it to zero
            resetLastMeasureCount()
            return 0
        else:
            myCount = int(myCount)
            return myCount

    def setLastMeasureCount(count):
        count = int(count)
        Prefs.set("JRM.meas.counter", count)


    imp = IJ.getImage()
    if imp == None:
        print("You need an image...")
        return
    else:
        roi = imp.getRoi()
        if roi != None:
            if roi.getType() == Roi.LINE:
                # print(roi)
                cal = imp.getCalibration()
                # print(cal)
                unit = cal.getUnits()
                width = cal.pixelWidth
                height = cal.pixelHeight
                x1 = roi.x1 * width
                y1 = roi.y1 * height
                x2 = roi.x2 * width
                y2 = roi.y2 * height
                length = sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
                if bDebug:
                    sOut = "X1: %d Y1 %d X2 %d Y2 %d" % (roi.x1, roi.y1,
                                                         roi.x2, roi.y2)
                    print(sOut)
                    print(length, unit)
                    
                ip = imp.getProcessor()
                ip.setColor(linCol)
                oldLW = ip.getLineWidth()
                ip.setLineWidth(lw)
                ip.drawLine(roi.x1, roi.y1, roi.x2, roi.y2)
                ip.setLineWidth(oldLW)
                imp.updateAndDraw()
                ol = imp.getOverlay()
                if ol == None:
                    ol = Overlay()
                res = imp.duplicate()
                # first a dummy text ROI to set the font
                tr = TextRoi(10, 10, "Foo")
                tr.setColor(labCol)
                tr.setFont("SanSerif", font, 1) 
                tr.setJustification(TextRoi.CENTER)
                tr.setAntialiased(True)
                # explicitly save preferences
                Prefs.savePreferences()
                xL = roi.x1 + roi.x2
                xL /= 2
                if offset < 0:
                    yL = min(roi.y1, roi.y2)
                    yL += offset
                else:
                    yL = max(roi.y1, roi.y2)
                    yL += offset
                length = round(length, digits)
                label = "%g %s" % (length, unit)
                tr = TextRoi(xL, yL, label)
                tr.setColor(labCol)
                tr.setFont("SanSerif", font, 1) 
                tr.setJustification(TextRoi.CENTER)
                tr.setAntialiased(True)
                ol.add(tr)
                imp.setOverlay(ol)
                imp.show()
                if csvPath != None:
                    if bAppend:
                        if os.path.isfile(csvPath):
                            theCount = GetLastMeasureCount() + 1
                            f=open(csvPath, 'a')
                        else:
                            f=open(csvPath, 'w')
                            resetLastMeasureCount()
                            theCount = 1
                            strLine = 'img, num, length (%s)\n' % unit
                            f.write(strLine)
                    else:
                        f=open(csvPath, 'w')
                        resetLastMeasureCount()
                        theCount = 1
                        strLine = 'img, num, length (%s)\n' % unit
                        f.write(strLine)
                    strLine = "%s, %d, %.6f\n" % (imp.getShortTitle(), theCount, length)
                    f.write(strLine)
                    f.close()
                    setLastMeasureCount(theCount)
                strMsg = "measured %s count = %d" % (imp.getShortTitle(), theCount)
                print(strMsg)

            else:
                print("You need a line ROI")

            # finally deselect
            IJ.run("Select None")




def autoThresholdBinarize(imp, method=Method.Otsu,
                          bWhite=True, bVerbose=False):
    """autoThresholdBinarize(imp, method=Method.Otsu,
                             bWhite=True, bVerbose=False)
    Auto Threshold an Image and return a binary image

    Parameters
    ----------
    imp: ImagePlus
        The Image Plus of the image to be thresholded
    method: An AutoThresholder.Method (Method.Otsu)
        The method to use to threshold the image
    bWhite: Boolean (True)
        If True, objects from gray levels thr:max are 1, othereise.
        objects from 0:thr are 1
    bVerbose: Boolean (False)
        If True, print the threshold value

    Return
    ------
    bin: ImagePlus
        The image plus of a binarized image (a duplicate)
    """
    cal = imp.getCalibration()
    wrk = imp.createImagePlus()
    ip = imp.getProcessor().duplicate().convertToByteProcessor()
    name = imp.getShortTitle() + '-bin'
    wrk.setProcessor(name, ip)
    stats = wrk.getStatistics()
    his = stats.histogram
    thr = AutoThresholder().getThreshold(method, his)
    if bVerbose:
        print(thr)
    if bWhite:
        ip.setThreshold(thr, stats.max, ImageProcessor.NO_LUT_UPDATE)
    else:
        ip.setThreshold(stats.min, thr, ImageProcessor.NO_LUT_UPDATE)
    # Call the Thresholder to convert the image to a mask
    IJ.run(wrk, "Convert to Mask", "")
    wrk.setCalibration(cal)
    wrk.setTitle(name)
    return wrk

def watershedBinaryImage(imp):
    """watershedBinaryImage(imp)
    Perform a watershed segmentation on a binary image

    Parameters
    ----------
    imp: ImagePlus
        The Image Plus of the image to be thresholded

    Return
    ------
    wat: ImagePlus
        The image plus of a segmented image (a duplicate)

    """
    cal = imp.getCalibration()
    wat = imp.createImagePlus()
    ip = imp.getProcessor().duplicate()
    name = imp.getShortTitle() + '-wat'
    wat.setProcessor(name, ip)
    EDM().toWatershed(ip)
    wat.setCalibration(cal)
    wat.setTitle(name)
    return wat

def anaCircParticles(imp, wat, csvPath, minArea=10, maxArea=100000, 
                     minCirc=0.35, maxAR=1.05, imgNo=1,
                     labFont=20, colOut=Color.red, colLab=Color.black,
                     bAppend=False, bVerbose=False):
    """
    imp, wat, csvPath, minArea=10, maxArea=100000, 
                     minCirc=0.35, maxAR=1.05, imgNo=1,
                     labFont=20, colOut=Color.red, colLab=Color.black,
                     bAppend=False, bVerbose=False)

    Analyze ROIs from system ROI Manager and Results Table and draw
    the desired features into a specified image.

    Parameters
    ----------
    imp: ImagePlus
        The ImagePlus of the original image
    wat: ImagePlus
        The ImagePlus of the watershed image
    csvPath: string
        Path for the output .csv file
    minArea : int (10)
        The minimum area to detect. Will be in units from calibration.
    maxArea : int (100000) 
        The maximum area to detect. Will be in units from calibration.
    minCirc : float (0.35)
        The minimum circularity to detect
    maxAR : float (1.05)
        The maximum aspect ratio to detect
    imgNo: int (1)
        Image number in series
    labFont: int (20)
        Font size
    colOut: Color (Color.red)
        Outline color
    colLab: Color (Color.black)
        Label color
    bAppend: Boolean (False)
        If True, append results to CSV file
    bVerbose: Boolean (False)
        If True, print info

    Return
    ------
    out: ImagePlus
        The ImagePlus of an original image with circular overlays
        drawn. Note: the data has been written to csvPath
    """
    jFont = Font("SanSerif", Font.BOLD, labFont)
    cal = imp.getCalibration()
    out = imp.createImagePlus()
    ip = imp.getProcessor().duplicate().convertToByteProcessor()
    name = imp.getShortTitle() + '-det'
    out.setProcessor(name, ip)
    out.setCalibration(cal)
    IJ.run(out, "Enhance Contrast", "saturated=0.0")

    # strMeas = "area centroid center fit shape redirect=None decimal=3"
    s1 = "area mean modal min centroid center perimeter bounding fit "
    s2 = "shape Feret's display redirect=None decimal=3" # % shortTitle
    strMeas = s1 + s2

    IJ.run(wat, "Set Measurements...", strMeas)
    # manual set...
    # "size=0-100000 circularity=0-1.00 display exclude clear add"
    # strAna = "display exclude clear add"
    s1 = "size=%g-%g display " % (minArea, maxArea)
    s2 = "exclude clear add"
    strAna = s1 + s2
    IJ.run(wat, "Analyze Particles...", strAna)
    rt = ResultsTable().getResultsTable()
    lArea = rt.getColumn(rt.getColumnIndex("Area"))
    lAR = rt.getColumn(rt.getColumnIndex("AR"))
    lCirc = rt.getColumn(rt.getColumnIndex("Circ."))
    lPeri = rt.getColumn(rt.getColumnIndex("Perim."))
    lRnd = rt.getColumn(rt.getColumnIndex("Round"))
    lSol = rt.getColumn(rt.getColumnIndex("Solidity"))
    lXm = rt.getColumn(rt.getColumnIndex("XM"))
    lYm = rt.getColumn(rt.getColumnIndex("YM"))
    roim = RoiManager.getInstance()
    
    nPart = len(lArea)
    partAR = []
    partID = []
    partECD = []
    partCir = []
    partPeri = []
    partRnd = []
    partSol = []
    lRois = []
    
    k=0
    i=0 # ROI and particle number
    # Try filtering ROIS by circularity
    for roi in roim.getRoisAsArray():
        area = lArea[i]
        circ = lCirc[i]
        xM = lXm[i]
        yM = lYm[i]
        ecd = 2.0 * math.sqrt(area/math.pi)
        if circ > minCirc:
            # save the feature vector
            partID.append(k+1)
            partECD.append(round(ecd, 4))
            partAR.append(lAR[i])
            partCir.append(lCirc[i])
            partPeri.append(lPeri[i])
            partRnd.append(lRnd[i])
            partSol.append(lSol[i])
            # append the ROI to the list
            lRois.append(roi)
            k += 1
        i += 1
    # clear the ROI manager and populate with 'good' particles
    # then draw each in the overlay...
    roim.reset()
    for i in range(len(lRois)):
        name = "%d" % (i+1)
        roi = lRois[i]
        roi.setName(name)
        roim.addRoi(roi)
        addRoiToOverlay(out, roi, label=name, bDrawLabels=True,
                        font=labFont, labCol=colLab, linCol=colOut)

    # Let's make certain everything displays properly...
    r = PointRoi(-10, -10)
    addRoiToOverlay(out, r, labCol=colLab, linCol=colOut)
    ovl = out.getOverlay()
    ovl.drawNames(True)
    ovl.drawLabels(True)
    out.updateImage()
    out.updateAndRepaintWindow()

    print(len(partID), len(partAR))

    # write the output file as .csv
    if bAppend:
        if os.path.isfile(csvPath):
            f=open(csvPath, 'a')
        else:
            f=open(csvPath, 'w')
            strLine = 'img, part, ecd, ar, cir, per, rnd, sol\n' 
    else:
        f=open(csvPath, 'w')
        strLine = 'img, part, ecd, ar, cir, per, rnd, sol\n'
        f.write(strLine)
    for k in range(len(partECD)):
        strLine  = "%d, %d, %.5f, " % (imgNo, partID[k], partECD[k])
        strLine += "%.5f, %.5f, "   % (partAR[k], partCir[k])
        strLine += "%.5f, %.5f, "   % (partPeri[k], partRnd[k])
        strLine += "%.5f\n"         % (partSol[k])
        f.write(strLine)
    f.close()
    return out



def applyGrayLimitsToFolder(folderPath, fLo, fHi, ext='.tif'):
    """
    applyGrayLimitsToFolder(folderPath, fLo, fHi, ext='.tif')

    Apply gray level limits to all images in a folder

    Parameters
    ----------
    folderPath : string
        The path to the folder to process. Expects a separator
        for the OS.

    fLo : number
        The lower gray level limit (black)

    fHi : number
        The upper gray level limit (white)

    ext : string, default '.tif'
        The file type to process

    Returns
    -------

    None

    Example
    -------

    import jmFijiGen as jmg
    jmg.applyGrayLimitsToFolder("C:\\Temp\\test\\", 1800, 11000, ext='.tif')
    """
    names = []
    for file in os.listdir(folderPath):
        if file.endswith(ext):
            name = os.path.splitext(file)[0]
            names.append(name)

    names.sort()

    for name in names:
        imgPath = folderPath + name + ext
        imp = IJ.openImage(imgPath)
        imp.show()
        ip = imp.getProcessor()
        ip.setMinAndMax(fLo, fHi)
        imp.updateImage()
        imp.setDisplayRange(fLo, fHi)
        imp.changes = False
        fs = FileSaver(imp)
        # let's make it platform agnostic
        if fs.saveAsTiff(imgPath):
            msg = "Tif saved successfully at " + imgPath
            print(msg) 
        imp.close()



def useSingleLUT(imp, bVerbose=False):
    """
    useSingleLUT(imp)

    Check an ImagePlus for a single LUT and activate if found

    Parameters
    ----------
    imp : ImagePlus
        The ImagePlus to be queried for a LUT and have the LUT activated

    bVerbose : A boolean flag (False)
        A flag for verbose messages

    Returns
    -------
        None

    Example:
    --------
    from ij import IJ
    import jmFijiGen as jmg
    IJ.run("M51 Galaxy (177K, 16-bits)")
    imp = IJ.getImage()
    jmg.useSingleLUT(imp, bVerbose=True)
    """
    if bVerbose:
        minV = imp.getDisplayRangeMin()
        maxV = imp.getDisplayRangeMax()
        sMsg = "Current display range: %g - %g" % (minV, maxV)
        print(sMsg)

    luts = imp.getLuts()
    lLUTS = len(luts)
    if (lLUTS == 1):
        if bVerbose:
            print(luts[0])
        imp.setLut(luts[0])
        imp.updateAndRepaintWindow()
    else:
        if bVerbose:
            if(lLUTS > 1):
                sMsg = "Found %g LUTs %s" % (lLUTS, luts)
                print(sMsg)
            else:
                print("No LUTs found")

def openFolderWithSingleLUT(folderPath, ext = '.tif'):
    """
    openFolderWithSingleLUT(folderPath, ext = '.tif')

    Open a folder of images and apply a saved LUT

    Parameters
    ----------
    folderPath : string
        The path to the folder to process. Expects a separator for the OS.

    ext : string, default '.tif'
        The file type to process

    Returns
    -------
        None

    Example
    -------

    import jmFijiGen as jmg
    jmg.openFolderWithSingleLUT("C:\\Temp\\test\\", ext='.tif')

    """
    names = []
    for file in os.listdir(folderPath):
        if file.endswith(ext):
            name = os.path.splitext(file)[0]
            names.append(name)

    names.sort()

    for name in names:
        imgPath = folderPath + name + ext
        imp = IJ.openImage(imgPath)
        useSingleLUT(imp)
        imp.show()



def correctCalibAspectRatio(imp, bVerbose=False):
    """
    correctCalibAspectRatio(imp, bVerbose=False)

    Correct the aspect ratio of a calibrated images that has different
    scale factors in X and Y directions.

    Parameters
    ----------
    imp: ImagePlus
        The image to correct
    bVerbose: Boolean (False)
        Flag to print info when True

    Returns
    -------
    impAR: ImagePlus
        The A/R corrected image
    
    """
    imp.show()
    h = imp.getHeight()
    w = imp.getWidth()
    cal = imp.getCalibration()
    aspectRatio = cal.pixelHeight/cal.pixelWidth
    newHeight = int(round(aspectRatio*h))
    if (bVerbose==True):
        print(aspectRatio)
        print(newHeight)

    newTitle = imp.getShortTitle() + "-arc"
    strArg31 = "x=- y=- width=%d height=%d " % (w, newHeight)
    strArg32 = "interpolation=Bicubic average create "
    strArg33 = "title=%s" % (newTitle)
    strArg3 = strArg31 + strArg32 + strArg33

    IJ.run(imp, "Scale...", strArg3)

    impAR = IJ.getImage()
    return impAR

def openRplRawImageCube(fDir, fName, width, height, nChan,
                        umPerPx, evPerCh, evOff):
    """
    openRplRawImageCube(fDir, fName, width, height, nChan,
                        umPerPx, evPerCh, evOff)

    Open a .raw Image Cube in LISPIX .rpl format

    Parameters
    ----------
    fDir: string
        The directory for the .raw file
    fName: string
        The file name for the .raw file
    width: int
        Slice width (px)
    height: int
        Slice height (px)
    nChan: int
        Number of slices
    umPerPx: float
        Microns per pixel for x- and y-axes
    evPerCh: float
        ev/ch for the EDS spectra at each pixel
    evOff: float
        eV offset for the spectra

    Returns
    -------
    tImp: ImagePlus
        A calibrated image stack
    """
    fi = FileInfo()
    # fi.fileType = fi.GRAY16_SIGNED
    fi.fileType = fi.GRAY16_UNSIGNED
    fi.fileFormat = fi.RAW
    fi.directory = fDir
    fi.fileName  = fName
    fi.width = width
    fi.height = height
    fi.nImages = nChan
    fi.gapBetweenImages = 0
    fi.intelByteOrder = True      # little endian
    fi.whiteIsZero = False        # no inverted LUT
    fi.longOffset = fi.offset = 0 # header size, in bytes
    fo = FileOpener(fi)
    imp = fo.open(False)
    cal = Calibration()
    cal.xOrigin = 0.
    cal.yOrigin = 0.
    cal.zOrigin = evOff/evPerCh
    cal.pixelWidth = umPerPx
    cal.pixelHeight = umPerPx
    cal.pixelDepth = evPerCh
    mu = IJ.micronSymbol
    scaUni    = mu + "m"
    cal.setXUnit(scaUni)
    cal.setYUnit(scaUni)
    cal.setZUnit("eV")
    tImp = ImagePlus()
    tImp.setStack(imp.getTitle(), imp.getStack())
    tImp.setCalibration(cal)
    IJ.run(tImp, "32-bit", "")
    stack = tImp.getImageStack()
    gMin = 32000.
    gMax = -32000.
    iMax = 0
    for i in xrange(1, tImp.getNSlices()+1):
        ip = stack.getProcessor(i)
        mV = ip.getMin()
        if (mV < gMin):
            gMin = mV
        mV = ip.getMax()
        if (mV > gMax):
            gMax = mV
            iMax = i
    IJ.setMinAndMax(tImp, gMin, gMax)
    # set to the channel with max intensity
    tImp.setPosition(iMax)
    print("Max intensity %.2f at channel %g" % (gMax, iMax ))
    return tImp

def correctForeshortening(imp, tiltDeg):
    """correctForeshortening(imp, tiltDeg)

    Correct the foreshortening in a tilted SEM image.
    Assumes tilt in the Y direction.

    Parameters
    ----------
    imp: ImagePlus
        The input image
    tiltDeg: float
        The tilt angle in degrees

    Returns:
    --------
    tiltCor: ImagePlus
        The tilt-corrected image.
    """
    ti = imp.getShortTitle() + "-tilt-cor"
    invCosTheta = 1.0/math.cos(math.pi*tiltDeg/180.)
    xNew = imp.getWidth()
    yNew = invCosTheta * imp.getHeight()
    strArg1 = "x=1.0 y=%.4f width=%d " (invCosTheta, xNew)
    strArg2 = "height=%d " % (yNew)
    strArg3 = "interpolation=Bicubic average create title=%s" % (ti)
    strArg = strArg1 + strArg2 + strArg3
    IJ.run(imp, "Scale...", strArg)
    tiltCor = IJ.getImage()
    return tiltCor

def medianFilter(imp, radPx):
    """medianFilter(imp, radPx)

    Perform a median filter on an image

    Parameters
    ----------
    imp: ImagePlus
        Input image
    radPx: number
        Filter radius (in pixels)

    Returns
    -------
    mf: ImagePlus
        The filtered image.
    """
    ti = imp.getShortTitle() + "-mf"
    IJ.run(imp, "Median...", "radius=%g" % radPx)
    mf = IJ.getImage()
    mf.setTitle(ti)
    return mf



def openOxfordRaw(strRaw, w, h, chan, strType="16-bit Signed"):
    """
    openOxfordRaw(strRaw, w, h, chan, strType="16-bit Signed")

    Open a .raw file exported by AZtec 3.0

    Parameters
    ----------
    strRaw: string
        Path to the .raw file
    w: int
        Stack width
    h: int
        Stack height
    chan: int
        Stack depth
    strType: string ("16-bit Signed")
        Stack data type

    Returns
    --------
    imp: ImagePlus
        The stack
    """
    s1 = "open=%s image=[%s] width=%d " % (strRaw, strType, w)
    s2 = "height=%d offset=0 number=%d " % ( h, chan)
    s3 = "gap=0 little-endian"
    strArg3 = s1 + s2 + s3
    IJ.run("Raw...", strArg3)
    imp = IJ.getImage()
    imp.show()
    return imp

def computeChannel(transEn, detGain=4.9833, detOff=-102.19):
    """
    computeChannel(transEn, detGain=4.9833, detOff=-102.19)

    Compute the channel for a peak a specified transition energy

    Parameters
    ----------
    transEn: float
        The X-ray transition energy in keV
    detGain: float (4.9833)
        The detector gain, in eV/Channel
    detOff: float (-102.19)
        The detector zero offset, in eV

    Returns
    -------
    chan: int
        The channel number for the peak transition energy
    """
    # first convert transEn to eV
    transEn *= 1000.
    chan = (transEn-detOff)/detGain
    chan = round(chan, 0)
    return int(chan)

def computeEnergy(chan, detGain=4.9833, detOff=-102.19):
    """computeChannel(chan, detGain=4.9833, detOff=-102.19)

    Compute the transition energy for a given channel

    Parameters
    ----------
    chan: int
        The channel number
    detGain: float (4.9833)
        The detector gain, in eV/Channel
    detOff: float (-102.19)
        The detector zero offset, in eV

    Returns
    -------
    transEn: float
        The transition energy in keV
    """
    # first convert transEn to eV
    transEn = detGain * float(chan) + detOff
    transEn /= 1000.
    transEn = round(transEn, 6)
    return transEn

def getStackSumSpectrum(imp, outDir="C:/Temp/tmp",
                        detGain=4.9833, detOff=-102.19,
                        owner="jrminter"):
    """
    getStackSumSpectrum(imp, outDir="C:/Temp/tmp",
                        detGain=4.9833, detOff=-102.19,
                        owner="jrminter")

    Get the sum spectrum for a stack, using a ROI if defined, and
    writing the results in a text file (MSA format).

    Parameters
    ----------
    imp: ImagePlus
        The input stack
    outDir: string ("C:/Temp/tmp")
        Output directory for the sum spectrum
    detGain: float (4.9833)
        Detector gain in eV/channel
    detOff: float (-102.19)
        Detector zero offset (channels)
    owner: string ("jrminter")
        Owner name for MSA format spectrum

    Returns
    -------
    None

    """
    roi = imp.getRoi()
    st = imp.getShortTitle()
    stack = imp.getStack()
    slices = imp.getNSlices()
    frames = imp.getNFrames()
    size = stack.getSize()
    cal = imp.getCalibration()
    analyzer = Analyzer(imp)
    strArg2 = "integrated redirect=None decimal=3"
    IJ.run(imp, "Set Measurements...", strArg2)
    measurements = Analyzer.getMeasurements()
    rt = Analyzer.getResultsTable()
    for i in range(size):
        imp.setSlice(i+1)
        ip = stack.getProcessor(i+1)
        ip.setRoi(roi)
        stats = ImageStatistics.getStatistics(ip, measurements, cal)
        analyzer.saveResults(stats, roi)
    lKeV =[]
    lIntens=[]
    rt.show("Results")
    nMeas = rt.getCounter()
    
    for i in range(nMeas):
        mc = rt.getColumnIndex("IntDen")
        intDen = rt.getValueAsDouble(mc, i)
        keV = computeEnergy(i+1, detGain, detOff)
        lKeV.append(keV)
        lIntens.append(intDen)
    tw = rt.getResultsWindow()
    tw.close(False)
    rt = ResultsTable()
    cKeV = rt.getFreeColumn("keV")
    cInt = rt.getFreeColumn("Intensity")
    for i in range(nMeas):
        rt.incrementCounter()
        rt.addValue(cKeV, lKeV[i])
        rt.addValue(cInt, lIntens[i])
    rt.show(st + "sum")

    now = datetime.datetime.now()
    sz = str(now)
    sp = sz.split(" ")
    sp0 = sp[0]
    sp1 =sp[1]
    sp2 = sp1.split(".")[0]

    # prepare the output file
    outPath = outDir + "/" + st + "-sum.msa"
    files = glob.glob(outPath)
    for file in files:
        os.unlink(file)
        print("deleting")
        time.sleep(2)
    
    f=open(outPath, 'w')
    strLine = "#FORMAT      : EMSA/MAS Spectral Data File"
    f.write(strLine +'\n')
    strLine = "#VERSION     : 1.0"
    f.write(strLine +'\n')
    strLine = "#TITLE       : %s" % st
    f.write(strLine +'\n')
    strLine = "#DATE        : %s" % sp0
    f.write(strLine +'\n')
    strLine = "#TIME        : %s" % sp2
    f.write(strLine +'\n')
    strLine = "#OWNER       : %s" % owner
    f.write(strLine +'\n')
    strLine = "#NPOINTS     : %g." % nMeas
    f.write(strLine +'\n')
    strLine = "#NCOLUMNS    : 1."
    f.write(strLine +'\n')
    strLine = "#XUNITS      : keV"
    f.write(strLine +'\n')
    strLine = "#YUNITS      : counts"
    f.write(strLine +'\n')
    strLine = "#DATATYPE    : XY"
    f.write(strLine +'\n')
    strLine = "#XPERCHAN    : %.6f" % float(detGain/1000.)
    f.write(strLine +'\n')
    strLine = "#OFFSET      : %.6f" % float(detOff/1000.)
    f.write(strLine +'\n')
    strLine = "#SIGNALTYPE  : EDS"
    f.write(strLine +'\n')
    strLine = "#SPECTRUM    : Spectral Data Starts Here"
    f.write(strLine +'\n')

    for k in range(len(lKeV)):
        strLine = "%.4f, %.2f\n" % (lKeV[k], lIntens[k] )
        f.write(strLine)

    strLine = "#ENDOFDATA   : "
    f.write(strLine +'\n')

    f.close()
    print("done!")


def bicubicRotate(imp, angDeg, bHeadless=False):
    """
    bicubicRotate(imp, angDeg, bHeadless=False)

    Rotate an image with bicubic interpolation and filling

    Parameters
    ----------
    imp: ImagePlus
        Input image
    angDeg: float
        Rotation angle (degrees); + for CW, - for CCW
    bHeadless: Boolean (False)
        Flagt to suppress display for headless operation

    Returns
    the Image Plus of a rotated image
    """
    if bHeadless == False:
        imp.show()
    cal = imp.getCalibration()
    ti = imp.getShortTitle()
    wrk = imp.duplicate()
    wrk.setCalibration(cal)
    sArg2 = "angle=%g grid=1 interpolation=Bicubic enlarge" % angDeg
    IJ.run(wrk, "Rotate... ", sArg2)
    wrk.setTitle(ti + "-rot")
    if bHeadless == False:
        wrk.show()
    return(wrk)



def horizProfileFromROI(imp, lRoi, sFact, outPathCsv,
                        iDigits=3, bHeadless=True):
    """
    horizProfileFromROI(imp, lRoi, sFact, outPathCsv,
                        iDigits=3, bHeadless=True)

    Generate an averaged horizontal profile from a rectangular ROI from
    an ImagePlus. Note: the image should be calibrated...

    Parameters
    ----------
    imp: ImagePlus
        Input image
    lRoi: list with 4 elements
        Parameters to construct the ROI
    sFact: float
        Scale factor, use 1 for pixels.
    outPathCsv: string
        Path to write a csv profile
    iDigits: int (3)
        Number of digits to round output
    bHeadless: Boolean (True)
        Flag to suppress display for headless operation

    Returns:
    --------
    impROI: list with two arrays
        Distance and intensity
    """
    if (len(lRoi) != 4):
        IJ.error("Not a proper rectangle","This function expects a 4 item list for the ROI")
        return None
    if bHeadless == False:
        imp.show()
    cal = imp.getCalibration()
    ti = imp.getShortTitle()
    na = "%s-roi[%d,%d,%d,%d]" % (ti, lRoi[0],lRoi[1],lRoi[2],lRoi[3])
    impROI = imp.duplicate()
    impROI.setCalibration(cal)
    impROI.setRoi(lRoi[0],lRoi[1],lRoi[2],lRoi[3])
    IJ.run(impROI,"Crop","")
    if bHeadless == False:
        imp.changes=False
        imp.close()
        impROI.setTitle(na)
        impROI.show()
    w = impROI.getWidth()
    h = impROI.getHeight()
    ip = impROI.getProcessor()
    ar = ip.getPixels()    
    x = []
    y = []
    gAvgMax = 0.
    for i in xrange(w):
        x.append(round(sFact*i, iDigits))
        gSum = 0.
        for j in xrange(h):
            iOff=j*w+i
            gVal = float(ar[iOff])
            gSum += gVal
        gAvg = gSum / float(h)
        if(gAvg > gAvgMax):
            gAvgMax = gAvg
        y.append(round(gAvg, 1))
    ret = [x,y]
    if bHeadless == False:
        impROI.changes = False

    f=open(outPathCsv, 'w')
    strLine = 'x.%s, intensity\n' % cal.getUnit()
    f.write(strLine)
    for k in range(len(x)):
        strLine = "%f, %f\n" % (x[k], y[k] / gAvgMax )
        f.write(strLine)
    f.close()
    return impROI

def anaLineFromXrayMap(imgPath, csvDir, unPerPx, units=-9,
                       startClean=True):
    """
    anaLineFromXrayMap(imgPath, csvDir, unPerPx, units=-9,
                       startClean=True)

    Loads an X-ray map from a vertical line, measures the thickness
    statistics, outputting them to a .csv file, and writing the detected
    edges into an overlay.

    Parameters
    ----------
    imgPath: string
        File to open
    csvDir: string
        Directory to write .csv file
    unPerPx: float
        Scale factor for each px
    units: int (-9)
        Power w.r.t meters. nm = -9
    startClean: Boolean (True)
        Flag. if True, all images are closed prior to execution.

    Returns:
    --------
    final: ImagePlus
        image with overlay

    """
    if (startClean==True):
        IJ.run("Close All")
    imp = IJ.openImage(imgPath)
    shortTitle = imp.getShortTitle()
    outPth = csvDir + "/" + shortTitle + ".csv"
    calibImageDirect(imp, unPerPx, units)
    imp.show()
    binary = binarizeXrayMap(imp)
    binary.show()
    IJ.run(binary, "Duplicate...", " ")
    edges = IJ.getImage()
    detectEdges(edges)
    edges.show()
    analyzeRois(edges, 5, outPth)
    binary.changes = False
    binary.close()
    forRed = shortTitle + "-2.tif"
    forGra = shortTitle + ".tif"
    # need to convert the map img to 8 bit for overlay
    IJ.run(imp,"8-bit","")
    strArg2 = "c1=%s c4=%s create" % (forRed, forGra)
    IJ.run("Merge Channels...", strArg2)
    comp = IJ.getImage()
    IJ.run("Stack to RGB")
    final = IJ.getImage()
    final.setTitle(shortTitle + "-ovl")
    final.show()
    comp.changes = False
    comp.close()
    return (final)


def findAndCloseImage(title):
    """
    findAndCloseImage(title)

    Find the image with the name `title' and immediately close it.

    Parameters
    ----------
    title: string
        Image to find and close

    Returns:
    --------
    None
    """
    imp = WindowManager.getImage(title)
    imp.changes = False
    imp.close()

def binarizeXrayMap(imp):
    """
    binarizeXrayMap(imp)

    For each row in an image of an oriented X-ray EDS map, find the 
    maximum value. Average these values to find the mean maximum
    intensity. Set the threshold and binarize the image.
    Return the binary image.

    Parameters
    ----------
    imp: ImagePlus
        Image to process

    Returns:
    --------
    wrk: ImagePlus
        Output image

    """
    IJ.run(imp, "Duplicate...", " ")
    wrk = IJ.getImage()
    # use a median filter to reduce noise
    IJ.run(wrk, "Median...", "radius=2")
    IJ.run(wrk, "32-bit", "")
    ip = wrk.getProcessor()
    w = ip.getWidth()
    h = ip.getHeight()
    print((w,h))
    pix = ip.getPixels()
    # an array to hold the maximum
    lMax = []
    # loop over the rows
    for j in range(h):
        mv = 0.
        for i in range(w):
            k = j*w+i
            test = pix[k]
            if (test > mv):
                mv = test
        lMax.append(mv)
    l = len(lMax)
    print(l)
    sum = 0.
    hi = 0.
    for i in range(l):
        v = lMax[i]
        sum += v
        if (v > hi):
            hi = v
    mv = sum / l
    print(mv, 2*hi)

    IJ.setThreshold(wrk, 0.5*mv, 2*hi)
    IJ.run(wrk, "Make Binary", "");
    IJ.run(wrk, "Convert to Mask", "");
    return(wrk)


def reduceMapNoise(imp):
    """reduceMapNoise(imp)

    Reduce the noise in an X-Ray EDS map using an ROF denoise.

    Parameters
    ----------
    imp: Image plus
        Input image

    Returns
    -------
    wrk: ImagePlus
        Output image (a duplicate)

    """
    wrk = imp.duplicate()
    IJ.run(wrk, "32-bit", "")
    IJ.run(wrk, "ROF Denoise", "theta=25")
    IJ.run(wrk, "16-bit", "")
    IJ.run(wrk, "Enhance Contrast...", "saturated=0")
    return wrk

def detectEdges(imp):
    """
    detectEdges(imp)

    Detect edges using a gradient squared, squared.


    Parameters
    ----------
    imp: Image plus
        Input image

    Returns
    --------
    wrk: ImagePlus
        Output image (a duplicate)

    """
    wrk = imp.duplicate()
    IJ.run(wrk, "32-bit", "")
    IJ.run(wrk, "Find Edges", "")
    IJ.run(wrk, "Square", "")    # turns the gradient into gradient squared
    IJ.run(wrk, "Square", "")    # further enhances the good edges
    IJ.run(wrk, "Enhance Contrast", "saturated=0")
    IJ.run(wrk, "8-bit", "")
    IJ.run(wrk, "Make Binary", "")
    return wrk

def detectMapLine(imp, thrMethod="Default dark"):
    """
    detectMapLine(imp, thrMethod="Default dark")

    Detects a line in an X-ray EDS map and converts the image to a Mask.

    Parameters
    ----------
    imp: Image plus
        Input image

    Returns
    --------
    wrk: ImagePlus
        Output image (a duplicate)

    """
    wrk = imp.duplicate()
    IJ.setAutoThreshold(wrk, thrMethod)
    IJ.run(wrk, "Convert to Mask", "")
    return wrk

def analyzeRois(imp, vAvg, outPath):
    """
    analyzeRois(imp, vAvg, outPath)

    Analyzes the calibrated input ImagePlus (imp) containing two
    lines at the edges, making  segments of height (vAvg), detecting the
    centroid of each edge and measuring the width. It writes a .csv file
    to outPath.

    Parameters
    ----------
    imp: Image plus
        Input image
    vAvg: int
        Height to analyse
    outPath: string
        Path for .csv file

    Returns
    --------
    None


    """
    w   = imp.getWidth()
    h   = imp.getHeight()
    cal = imp.getCalibration()
    n = h/vAvg

    # create empty output vectors for results
    lRoi = []
    lLw  = []

    for i in range(n):
        rt = ResultsTable.getResultsTable()
        rt.reset()
        impROI = imp.duplicate()
        impROI.setCalibration(cal)
        impROI.setRoi(0,vAvg*i,w,vAvg)
        IJ.run(impROI,"Crop","")
        IJ.run(impROI, "Make Binary","")
        impROI.show()
        IJ.run(impROI, "Set Measurements...", "center redirect=None decimal=3")
        IJ.run(impROI, "Analyze Particles...", "size=3-200 pixel clear add")
        nMeas = rt.getCounter()
        if (nMeas == 2):
            mc = rt.getColumnIndex("XM")
            l = rt.getValueAsDouble(mc, 0)
            r = rt.getValueAsDouble(mc, 1)
            lw = abs(r - l)
            lRoi.append(i+1)
            lLw.append(lw)
        print((i,lw))

        impROI.changes = False
        impROI.close()

    # prepare the output file
    f=open(outPath, 'w')
    strLine = 'n, width.%s\n' % cal.getUnit()
    f.write(strLine)
    for k in range(len(lRoi)):
        strLine = "%d, %.2f\n" % (lRoi[k], lLw[k] )
        f.write(strLine)

    f.close()

def corImageFIB(imp, umPerPx):
    """ corImageFIB(imp, umPerPx)
    Correct the aspect ratio of a FIB image stitched with analySIS 5.0.

    Note: FEI and SIS did/do some undocumented image manipulation under
    the hood. This was worked out using analySIS to stitch the base image
    and then correcting for their misdeeds. Their code reproducibly scales
    the height by a factor of 1.154135.

    Parameters
    ----------
    imp: Image plus
        Input image
    umPerPx: float
        Scale factor (microns/px)

    Returns
    --------
    None (works 'in-place')
    """

    mu = IJ.micronSymbol
    scaUni    = mu + "m"

    ti = imp.getShortTitle() + "-arc"
    wd = imp.getWidth()
    ht = imp.getHeight()
    newHt = int(round(1.154135*ht,0))
    s1 = "x=- y=- width=%d height=%d " % (wd, newHt)
    s2 = "interpolation=Bicubic average create title=%s" % (ti)
    strArg = s1 + s2
    IJ.run("Scale...", strArg);
    strArg = "distance=1 known=%f pixel=1 unit=%s" % (umPerPx, scaUni)
    IJ.run("Set Scale...", strArg)

def addRoiToOverlay(imp, roi, label=None, bDrawLabels=False, font=20,
                    labCol=Color.white, linCol=Color.white):
    """
    addRoiToOverlay(imp, roi, label="", bDrawLabels=False, font=20,
                    labCol=Color.white, linCol=Color.white)

    A convenience function to draw a ROI into the overlay of an
    ImagePlus. This is useful for situations where ROIs are computed
    from a highly processed image and the analyst wants to
    draw them into the overlay of the original image (e.g. particle
    analysis after a watershed separation. Adapted from addToOverlay()
    from Analyzer.java

    Parameters
    ----------
    imp: ImagePlus
        Image into which we draw the ROI
    roi: ROI
        ROI to draw
    label: string (None)
        Optional label
    bDrawLabels: Boolean (False)
        Flag to draw ROI labels
    font: int
        Font size for label
    labCol: Color (Color.white)
        Color for the label
    linCol: Color (Color.white)
        Color for the stroke/line

    Returns
    -------
    imp: ImagePlus
        Image with the updated overlay
    """
    jFont = Font("SanSerif", Font.BOLD, font)
    roi.setIgnoreClipRect(True)
    ovl = imp.getOverlay()
    if ovl == None:
        ovl = Overlay()
    ovl.drawNames(bDrawLabels)
    ovl.drawLabels(bDrawLabels)
    ovl.setLabelFont(jFont) 
    ovl.setStrokeColor(linCol)
    ovl.setLabelColor(labCol);
    ovl.drawBackgrounds(False);
    ovl.add(roi)
    imp.setOverlay(ovl)
    imp.updateImage()
    return imp

def anaParticlesWatershed(imp, strThrMeth="method=Default white",
                          minArea=10, maxArea=100000,
                          minCirc=0.35, maxAR = 1.05,
                          labCol=Color.white, linCol=Color.green,
                          bDebug=False, bFillHoles=False,  sl=0.005):
    """
    anaParticlesWatershed(imp, strThrMeth="method=Default white",
                          minArea=10, maxArea=100000,
                          minCirc=0.35, maxAR = 1.05,
                          labCol=Color.white, linCol=Color.green,
                          bFillHoles=False, bDebug=False, sl=0.005)

    A wrapper function to do particle analysis from an image after a
    watershed transformation and draw the detected features into the
    overlay of the original image.


    Parameters
    ----------
    imp : ImagePlus
        The image to process
    strThrMeth : string ('method=Default white')
        Used to specifying the threshold method
    minArea : int (10)
        The minimum area to detect. Will be in units from calibration.
    maxArea : int (100000) 
        The maximum area to detect. Will be in units from calibration.
    minCirc : float (0.35)
        The minimum circularity to detect
    maxAR : float (1.05)
        The maximum aspect ratio to detect
    labCol : color (Color.white)
        The color for labels in the overlay
    linCol : color (Color.green)
        The color for line/stroke in the overlay
    bDebug : boolean (False)
        A flag that, if true, keeps the work image open
    bFillHoles : boolean (False)
        A flag to fill holes in the detected image
    sl : float (0.005)
        Time to sleep when adding ROIs to not overload.

    Returns
    -------
    rt : a results table
        The results table for further processing.
    """
    title = imp.getTitle()
    shortTitle = imp.getShortTitle()
    
    typ = imp.getType()
    imp.setTitle(shortTitle)
    imp.show()
    IJ.run(imp,"Duplicate...", "title=work")
    wrk = IJ.getImage()
    # if this is a 16 bit image, convert to 8 bit prior to threshold
    if typ == ImagePlus.GRAY16:
        IJ.run(wrk, "Enhance Contrast", "saturated=0.35")
        IJ.run(wrk, "8-bit", "")
    IJ.run(wrk, "Threshold", strThrMeth)
    if bFillHoles == True:
        IJ.run(wrk, "Fill Holes", "")
    IJ.run(wrk, "Watershed", "")
    wrk.show()
    s1 = "area mean modal min center perimeter bounding fit shape "
    s2 = "Feret's display redirect=%s decimal=3" % shortTitle
    strMeas = s1 + s2
    IJ.run(wrk, "Set Measurements...", strMeas)
    s1 = "size=%d-%d circularity=%g-1.00" % (minArea, maxArea, minCirc)
    s2 = "    exclude clear include add"
    strAna = s1 + s2
    IJ.run(wrk, "Analyze Particles...", strAna)
    rt = ResultsTable().getResultsTable()
    
    lAspRat = rt.getColumn(rt.getColumnIndex("AR"))
    rm = RoiManager.getInstance()
    ra = rm.getRoisAsArray()
    # Let's draw the particles into the overlay of the original
    i=0
    for r in ra:
        i += 1
        rLab = "%d" % i
        r.setName(rLab)
        # only if the aspect ratio is OK
        if lAspRat[i-1] <= maxAR:
            imp = addRoiToOverlay(imp, r, labCol=labCol, linCol=linCol)
        # needed to put in sleep here on cruch to let this complete
        # and not overrun buffer
        time.sleep(sl)
    # let's put a PointRoi outside the image to get the overlays
    # all the same color
    r = PointRoi(-10, -10)
    imp = addRoiToOverlay(imp, r, labCol=labCol, linCol=linCol)
    # clear the roi manager and return the results table
    rm.reset()
    rm.close()
    if bDebug == False:
        wrk.changes = False
        wrk.close()
    imp.setTitle(title)
    return rt


def smoothMapImage(imp, no=2):
    """
    smoothMapImage(imp, no=2)

    Parameters
    ----------
    imp : ImagePlus
        Input image
    no: number (2)
        The noise offset to remove noise pixels
    Returns
    -------
    ret: ImapePlus
        The 8-bit, scaled, filtered image

    Algorithm Information
    ---------------------

    Smooths an X-ray map image (typically a 16 bit gray image). First,
    it sets the display range to a noise offset to the max and sets
    pixels below the noise offset to zero (to get rid of isolated
    pixels), converts to an 8 bit image that spans no to 255 and
    smooths with a 3x3 kernel. It then converts it to an 8 bit gray
    scale image that spans 0-255. This is ready for a hueLUT. It
    performs this on a duplicate image and returns the result.

    To the best of my understanding, this is how Oxford
    treats their maps. 
    """
    stats = imp.getStatistics(Measurements.MIN_MAX)
    imp.setDisplayRange(no, stats.max)
    ret = imp.duplicate()
    ip = ret.getProcessor()
    data = ip.getPixels()
    l = len(data)
    for i in range(l):
        val = data[i]
        if val < no:
            data[i] = 0
    IJ.run(ret, "8-bit", "")
    name = imp.getShortTitle()
    ip = ret.getProcessor()
    ip.smooth()
    stats = ret.getStatistics(Measurements.MIN_MAX)
    ret.setDisplayRange(0, stats.max)
    ret.setTitle(name)
    return ret
    
def clipNoisePixMapImage(imp, no=2):
    """clipNoisePixMapImage(imp, no=2)

    Parameters
    ----------
    imp : ImagePlus
        Input image
    no: number (2)
        The noise offset to remove noise pixels
    Returns
    -------
    ret: ImapePlus
        The 8-bit, scaled, clipped image

    Algorithm Information
    ---------------------

    Clips noise pixels from an X-ray map image (typically a 16 bit gray
    image).  First, it sets the display range to a noise offset to max
    and removes the noise pixels (to get rid of isolated pixels), then
    converts to an 8 bit image that spans 0 to 255 and returns an 8 bit
    gray scale image. This is ready for a hueLUT.
    """
    stats = imp.getStatistics(Measurements.MIN_MAX)
    imp.setDisplayRange(no, stats.max)
    ret = imp.duplicate()
    ip = ret.getProcessor()
    data = ip.getPixels()
    l = len(data)
    for i in range(l):
        val = data[i]
        if val < no:
            data[i] = 0
    IJ.run(ret, "8-bit", "")
    name = imp.getShortTitle()
    stats = ret.getStatistics(Measurements.MIN_MAX)
    ret.setDisplayRange(0, stats.max)
    ret.setTitle(name)
    return ret

def headlessCropStack(imp, lRoi):
    """
    headlessCropStack(imp, lRoi)

    Crop a stack to a rectangle given by the list, lRoi

    Parameters
    ----------
    imp:  ImagePlus
        The stack to crop
    lRoi: a list
        Contains [x0, y0, w, h]

    Returns
    -------
    imp: ImagePlus
        The cropped stack
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

def makeStackFromImageFiles(lNames, imgDir, stkName='stack',
                            ext='.tif', bUseStackHisto=False):
    """
    makeStackFromImageFiles(lNames, imgDir, stkName='stack',
                            ext='.tif', bUseStackHisto=False)

    Construct a stack of images from a list of file names.

    Parameters
    ----------
    lNames: list
        Base file names to process
    imgDir: string
        Path to the image files
    stkName : string ('stack')
        Name for the stack
    ext: string ('.tif')
        File extension
    bUseStackHisto: Boolean (False)
        Flag to use the same LUT for the whole stack 

    Returns
    -------
    ret: ImagePlus
        The generated stack
    """
    strImg = imgDir + "/" + lNames[0] + ext
    imp = IJ.openImage(strImg)
    newStack = ImageStack(imp.getWidth(), imp.getHeight())
    for name in lNames:
        strImg = imgDir + "/" + name + ext
        imp = IJ.openImage(strImg)
        newStack.addSlice(name, imp.getProcessor())
    ret = ImagePlus(stkName, newStack)
    if bUseStackHisto == True:
        sArg2 = "saturated=0.35 process_all use"
        IJ.run(ret, "Enhance Contrast", sArg2)
    else:
        sArg2 = "saturated=0.35 process_all"
        IJ.run(ret, "Enhance Contrast", sArg2)
    return ret


def headlessFlatten(imp):
    """headlessFlatten(imp)

    A flatten command that works in headless mode.

    Parameters
    ----------
    imp: ImagePlus
        Image to flatten
    
    Returns
    -------
    ret: ImagePlus
        The flattened image
    """
    flags = imp.isComposite()
    if flags==False:
        IJ.setupDialog(imp, 0)
    ret = imp.flatten()
    ret.setTitle(imp.getShortTitle())
    return ret

def makeFlattenedTransparentOverlay(impBase, impOvr, op=50):
    """
    makeFlattenedTransparentOverlay(impBase, impOvr, op=50)

    Make a transparent overlay on an image and flattens it.
    Note: Cannot be headless because of the flatten.

    Parameters
    ----------
    impBase: ImagePlus
        The underlying image (uses a duplicate)
    impOvr: ImagePlus
        The image to overlay
    op: number (50)
        The percent opacity

    Returns
    -------
    imp: ImagePlus
        The flattened composite image
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

    Make a RGB stack from a list of RGB images

    Parameters
    ----------
    lImps: list of ImagePlus
        From RGB images to create the stack
    strName: string ('Stack')
        Name for the stack

    Returns
    -------
    impStack: ImagePlus
        The stack
    """
        
    w = lImps[0].getWidth()
    h =    lImps[0].getHeight()
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
        stack.addSlice(lImps[i].getShortTitle(),
                       lImps[i].getProcessor().convertToRGB())
    stack.update(lImps[0].getProcessor())
    impStack = ImagePlus(strName, stack)
    impStack.setCalibration(cal)
    fi.fileName = ""
    fi.nImages = impStack.getStackSize()
    impStack.setFileInfo(fi) 
    return impStack

def printJavaVersion():
    """
    printJavaVersion()

    Check and print the Java version
    """
    ans="bad"
    if IJ.isJava16():
        ans = "Java 1.6"
        if IJ.isJava17():
            ans = "Java 1.7"
            if IJ.isJava18():
                ans = "Java 1.8"
    print ans                

def scaleImg(imp,factor):
    """
    scaleImg(imp,factor)

    Scale an input ImagePlus for an image by factor using
    bicubic interpolation.

    Parameters
    ----------
    imp: ImagePlus
        Input image
    factor: float
        Scaling factor

    Returns
    -------
    imp2: ImagePlus
        Scaled image
    """

    name = imp.getShortTitle()
    averageWhenDownsizing = True
    im = ImageProcessor.BICUBIC
    newWidth = int(round(factor*imp.getWidth(), 0))
    newHeight = int(round(factor*imp.getHeight(), 0))
    ip = imp.getProcessor()
    ip.setBackgroundValue(0)
    imp2 = imp.createImagePlus()
    imp2.setProcessor(name, ip.resize(newWidth, newHeight,
                      averageWhenDownsizing))
    cal = imp2.getCalibration()
    cal.pixelWidth *= 1.0/factor
    cal.pixelHeight *= 1.0/factor    
    return imp2


def labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24,
                 col=Color.WHITE, bHeadless=False):
    """
    labelMontage(imp, lLabels, cols, rows, w0=12, h0=2, font=24,
                 col=Color.WHITE, bHeadless=False)

    Label a montage in the overlay

    Parameters
    ----------
    imp       - the ImagePlus of the montage to label
    lLabels   - a list of labels to write into the overlay
    cols      - the number of columns in the montage
    rows      - the number of rows in the montage
    w0        - the x offset for the label (defaults to 12 px)
    h0        - the y offset for the label (defaults to    2 px)
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
    
 
def RGBtoMontage(imp, font=24, col=Color.WHITE,
                 bClose=True, bHeadless=False):
    """
    RGBtoMontage(imp, font=24, col=Color.WHITE,
                 bClose=True, bHeadless=False)

    Split an RGB image into channels, convert each to RGB, and then
    make a montage of the four images.

    Parameters
    ----------
    imp: ImagePlus
        The montage to label
    font: int (24)
        Size of the font (pts, defaults to 24)
    col: Color (Color.WHITE)
        Text color 
    bClose: Boolean (True)
        Flag to close the input image when no longer needed.
    bHeadless: Boolean (False)
        Flag to suppress display for headless mode

    Returns
    -------
    impMont: ImagePlus
        Labeled, duplicate of the input image
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
    # makeMontage2(ImagePlus imp, int columns, int rows, double scale,
    # int first, int last, int inc, int borderWidth, boolean labels) 
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

    trR = TextRoi(        10, 0, "R")
    trR.setColor(col)
    trR.setFont("SanSerif", font, 1) 
    trR.setJustification(TextRoi.CENTER)
    trR.setAntialiased(True)
    
    trG = TextRoi(    w+10, 0, "G")
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
    """
    findI0(imp, maxSearchFrac=0.5, chAvg=5)

    Search a single channel image from the maximum gray level down
    to find the mean intensity.

    Parameters
    ----------
    imp: ImagePlus
        Input image
    maxSearchFrac: float < 1.0 (0.5)
        Maximum fraction of gray space to search
    chAvg: int (5)
        Number of channels on either side of the maximum
        to average to find the centroid.

    Returns
    -------
    iZero: float
        The mean intensity of the peak or None if there is an error.
    """
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
    Check if a number is NaN

    Parameters
    ----------
    num: a number
        value to check

    Returns
    -------
    Boolean
    """
    return num != num

def checkNaN(x):
    """checkNaN(x)

    This checks if a value (e.g. K-ratio) is NaN and sets the value to
    zero if it is. This really helps when writing data frames to be
    read by R.

    Parameters
    ----------
    x: number

    Returns
    -------
    x or zero
    """
    if isNaN(x):
        x = 0.0
    return x
    

def i2b(i):
    """i2b(i)

    Convert an integer to a byte. Useful for LUTs.

    Parameters
    ----------
    i: int
        Input

    Returns
    -------
    i: byte
        Converted integer
    """
    if i > 127:
        i -= 256
    if i < -128:
        i = 128
    return i

def burnBox(imp, lRoi, col="green", wid=2):
    """
    burnBox(imp, lRoi, col="green", wid=2)

    Burn a box into an ImagePlus

    Parameters
    ----------
    imp: ImagePlus
        Input image
    lRoi: list
        ROI parameters: [x0, y0, w, h]
    col: string ("green")
        Text color representation
    wid: int (3)
        Line width

    Returns
    -------
    None
    """
    roi = Roi(lRoi[0], lRoi[1], lRoi[2], lRoi[3])
    imp.setRoi(roi)
    strStroke = "    stroke=%s width=%g" % (col, wid)
    IJ.run(imp, "Properties... ", strStroke )
    IJ.run(imp, "Add Selection...", "")

def hueDegToRGBCol(hue):
    """
    hueDegToRGBCol(hue)

    Convert a hue value (0 to 360 degrees) to an RGB color.
    Useful for LUTs.

    Parameters
    ----------
    hue: float 0. < hue < 360.
        Hue value

    Returns
    -------
    ret: RGB color
    """
    h = hue / 360.
    [r, g, b] =    hsv_to_rgb(h, 1.0, 1.0)
    ret = [255.0*r, 255.0*g, 255.0*b]
    return ret
    
def applyHueLUT(imp, hueDeg, gamma=1.0, bHeadless=False):
    """
    applyHueLUT(imp, hueDeg, gamma=1.0, bHeadless=False))

    Create and a apply a LUT to an ImagePlus where the maximum
    intensity corresponds to the hue specified by hueDeg. Optionally
    apply a gamma.

    Parameters
    ----------
    imp: ImagePlus
        Input image
    hueDeg: float
        hue angle, in degrees, 0 <=  hueDeg < 360
    gamma: float (1.0)
        Optional gamma correction
    bHeadless: Boolean (False)
        Flag, suppresses display when True for headless mode

    Returns
    -------
    ret: ImagePlus
        Image with the new LUT applied
    """
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
    """
    getUnitString(units)

    Get a unit string given a power

    Parameters
    ----------
    units: integer (-6)
        Exponent for unit w.r.t. meters

    Returns
    -------
    scaUni: string
        The unit string
    """
    if(units == -6):
        mu = IJ.micronSymbol
        scaUni    = mu + "m"
    if(units == -3):
        scaUni    = "mm"
    if(units == -9):
        scaUni    = "nm"
    if(units == -10):
        scaUni    = IJ.angstromSymbol
    if(units == 0):
        scaUni    = "m"
    if(units == 3):
        scaUni    = "km"
    return(scaUni)


def vertProfileFromROI(imp, lRoi, sFact, bHeadless=True):
    """
    vertProfileFromROI(imp, lRoi, sFact, bHeadless=True)

    Generate an averaged vertical profile from a rectangular ROI
    and an image.

    Parameters
    ----------
    imp: ImagePlus
        Input image
    lRoi: list
        ROI parameters: [x0, y0, w, h]
    sFact: float (1.0)
        Scale factor, defaults to 1 for pixels.
    bHeadless: Boolean (True)
        Flag to suppress display for headless operation

    Returns
    -------
    [x,y]: list
        List with distance and intensity arrays
    """
    if (len(lRoi) != 4):
        msg = "This function expects a 4 item list for the ROI"
        IJ.error("Not a proper rectangle", msg)
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
    """
    procAZtecTifMap(imp, colStr, gamma=1.0, theta=5)

    Process an ImagePlus from an AZtec X-ray map exported as a TIF

    Parameters
    ----------
    imp: ImagePlus
        Input image
    colStr: string
        color for the LUT
    gamma: float (1.0)
        Gamma transform for the map
    theta : float (5.0)
        Parameter for ROF denoising.

    Returns
    -------
    impRet: ImagePlus
        The transformed image
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
    """
    calStackZ(imp, scaleX, scaleY, scaleZ, units=-6, bVerbose=False)

    Calibrate a stack from it's ImagePlus and scale factors

    Parameters
    ----------
    imp: ImagePlus
        Input image
    scaleX: float
        scale factor for the width
    scaleY: float
        scale factor for the height
    scaleZ: float
        scale factor for the depth
    unit: int (-6)
        Power for the units w.r.t. meters

    Returns
    -------
    imp: ImagePlus
        The calibrated stack
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
    cal.pixelWidth    = scaleX
    cal.pixelHeight = scaleY
    cal.pixelDepth    = scaleZ
    imp.setCalibration(cal)
    
    # imp.updateAndRepaintWindow() 

    if(bVerbose):
        print(nS)
        print(cal)
    
    return imp

def whiteBalance(imp, bVerbose=False):
    """
    whiteBalance(imp, bVerbose=False)

    White balance an image from a ROI.
    Requires a ROI of the neutral area.

    Adapted from the macro by Vytas Bindokas; Oct 2006, Univ. of Chicago

    Parameters
    ----------
    imp: ImagePlus
        Input image
    bVerbose: Boolean, (False)
        Whether to print info

    Returns
    -------
    imp: ImagePlus
        The corrected image (displayed).
    """
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
        IJ.run("Add...",    strSlice )
    if (dG>0):
        IJ.run("Subtract...",    strSlice )

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

    Parameters
    ----------
    lis: list or vector
        Input array

    Returns
    -------
    [mu, sd, count] as a vector
    """
    count = len(lis)
    mu = sum(lis) / float(count)
    s = 0
    for i in range(count):
        s += pow(lis[i] - mu, 2)
    sd = math.sqrt(s / float(count -1))
    res = [mu, sd, count]
    return res
    

def ensureDir(d):
    """
    ensureDir(d)

    Check if the directory, d, exists, and if not create it.

    Parameters
    ----------
    d: string
        Path to check

    Returns
    -------
    None

    """
    if not os.path.exists(d):
        os.makedirs(d)
        
def makeTmpDir():
    """
    makeTmpDir()

    Make a working directory in $IMG_ROOT and make sure it is clean.

    Parameters
    ----------
    None

    Return
    ------
    None
    """
    imgDir = os.environ['IMG_ROOT']
    tmpDir = imgDir + "/tmp"
    ensureDir(tmpDir)
    strPath = tmpDir + "/*.*"
    files = glob.glob(strPath)
    for file in files:
        os.unlink(file)
    return tmpDir
    
def makeMontage(lNames, columns, rows, inDir, inExt= ".png",
                sca=1.0, lCal=[], lCr=None,
                bDebug=False, bHeadless=False):
    """
    makeMontage(lNames, columns, rows, inDir, inExt= ".png",
                sca=1.0, lCal=[], lCr=None,
                bDebug=False, bHeadless=False)

    Make a montage from a list of file names

    Parameters
    ----------
    lNames: list
        A list of file names
    columns: int
        number of columns in the montage
    rows: int
        number of rows in the montage
    inDir: string
        Path to input directory for images
    inExt: string ('.png')
        Input extension for images
    sca: float (1.0)
        Scale factor
    lCal: list ([])
        Optional list of calibration info:
        [fullWidth, imgImgWidthPx, -6]
    lCr: list (None)
        Optional list of parameters for a crop [x0,y0,w, h]
    bDebug: Boolean (False)
        Flag to print diagnostic info
    bHeadless Boolean (False)
        Suppress display for headless mode

    Returns
    -------
    impMont: ImagePlus
        The montage
    """
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
    # makeMontage2(ImagePlus imp, int columns, int rows, double scale,
    #              int first, int last, int inc, int borderWidth,
    #              boolean labels) 
    impMont = mont.makeMontage2(impStack, columns, rows, sca,
                                1, l, 1, 0, False)
    # strMon = "columns=%g rows=%g scale=%f first=1 last=%d increment=1
    #            border=0 font=12" % (columns, rows, sca, l)
    # IJ.run("Make Montage...", strMon)
    if (bDebug==False):
        impStack.changes = False
        impStack.close()
    if (l2 == 3):
            impMont = calibAZtecImage(impMont, lCal[0], lCal[1], units=lCal[2])
    return impMont
    
def calibImage(theImp, fullWidth, units=-6):
    """
    calibImage(theImp, fullWidth, units=-6)

    Calibrate the ImagePlus

    Parameters
    ----------
    theImp: ImagePlus
        Image to calibrate
    fullWidth: float
        The full width of the image, typically in microns
    units: int (-6)
        The exponent w.r.t. meters;  -6 is microns

    Returns
    -------
    theImp: ImagePlus
        The calibrated image
    """
    scaUni = getUnitString(units)
    w = float(theImp.getWidth())
    sf = fullWidth/w
    cal = theImp.getCalibration()
    cal.setXUnit(scaUni)
    cal.setYUnit(scaUni)
    cal.pixelWidth    = sf
    cal.pixelHeight = sf
    theImp.setCalibration(cal)
    # s1 = "distance=%d known=%f unit=%s" % (w, fullWidth, scaUni)
    # IJ.run(theImp, "Set Scale...", s1)
    return theImp

def calibImageDirect(theImp, unPerPx, units=-6):
    """
    calibImage(theImp, unPerPx, units=-6)

    Directly calibrate the ImagePlus

    Parameters
    ----------
    theImp: ImagePlus
        Image to calibrate
    unPerPx: float
        The spacing between pixels in units
    units: int (-6)
        The exponent w.r.t. meters. -6 = microns...

    Returns
    -------
    theImp:  ImagePlus
        The calibrated image
    """
    scaUni = getUnitString(units)
    cal = theImp.getCalibration()
    cal.setXUnit(scaUni)
    cal.setYUnit(scaUni)
    cal.pixelWidth = unPerPx
    cal.pixelHeight = unPerPx
    # theImp.setCalibration(cal)
    # w = theImp.getWidth()
    # s1 = "distance=1 known=%f unit=%s" % (unPerPx, scaUni)
    # IJ.run(theImp, "Set Scale...", s1)
    return theImp

def calibAZtecImage(theImp, fullWidth, baseImgWidth, units=-6):
    """
    calibAZtecImage(theImp, fullWidth, baseImgWidth, units=-6)

    Calibrate the ImagePlus using the AZtec convention of a full
    width in sample space and a base image width.

    Parameters
    ----------
    theImp: ImagePlus
        Image to calibrate
    fullWidth: float
        The full width of the image, typically in microns
    baseImgWidth: int
        The width, in px, of the base image
    units: int (-6)
        The exponent w.r.t. meters. -6 = microns...

    Returns
    -------
    theImp: ImagePlus
        The calibrated image
    """
    scaUni = getUnitString(units)
    w = float(baseImgWidth)
    sf = fullWidth/w
    cal = theImp.getCalibration()
    cal.setXUnit(scaUni)
    cal.setYUnit(scaUni)
    cal.pixelWidth    = sf
    cal.pixelHeight = sf
    theImp.setCalibration(cal)
    # s1 = "distance=%d known=%f unit=%s" % (baseImgWidth, fullWidth, scaUni)
    # IJ.run("Set Scale...", s1)
    return theImp

def doCrop(theImp, lPar):
    """
    doCrop(theImp, lPar)

    Crop an ImagePlus to a rectangle.

    Parameters
    ----------
    theImp: ImagePlus
        Input image
    lPar: list
        ROI parameters[x0,y0,width,height]

    Returns
    -------
    theImp: ImagePlus
        The calibrated image
    """
    if (len(lPar) != 4):
        IJ.log("You need to pass a list of 4 int [x,y,w,h] to doCrop")
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

def makeStackFromDir(inpDir, inExt='.tif', bDebug=False):
    """
    makeStackFromDir(inpDir, inExt='.tif', bDebug=False)

    Make a stack from all files in a directory

    Parameters
    ----------
    inpDir: string
        Input directory
    inExt: string ('.tif')
        Input file extension
    bDebug: Boolean (False)
        Flag to print info if True

    Returns
    -------
    impStack: ImagePlus
        The stack
    """
    for file in os.listdir(inpDir):
        if file.endswith(inExt):
            path = inpDir + "/" + file
            raw = IJ.openImage(path)
            raw.show()
    IJ.run("Images to Stack")
    impStack = WindowManager.getCurrentImage()
    return impStack
    
def addScaleBar(theImp, scaFac, scaUni,
                barWid, barHt, barFnt, barCol, barLoc):
    """
    addScaleBar(theImp, scaFac, scaUni,
                barWid, barHt, barFnt, barCol, barLoc)

    Add a scale bar to an image

    Parameters
    ----------
    theImp: ImagePlus
        The input image
    scaFac: float
        Scale factor in units/px
    scaUni: string
         Scale units, e.g. "nm"
    barWid: float
        Bar width (units), e.g. 100
    barHt: int
        Bar height (px), e.g. 9
    barFnt: int
        Bar font, e.g. 48
    barCol: string
        Bar color, e.g. "White"
    barLoc: string
        Bar location, e.g. "Lower Right"
    """
    theImp.show()
    foo = theImp.duplicate()
    s1 = "distance=1 known=%f unit=%s" % (scaFac, scaUni)
    IJ.run(theImp, "Set Scale...", s1)
    s2a = "width=%g height=%g " % (barWid, barHt)
    s2b = "font=%g color=%s " % (barFnt, barCol)
    s2c = "location=[%s] bold" % (barLoc)
    s2 = s2a + s2b + s2c
    # dummy to get things set
    IJ.run(foo, "Add Scale Bar", s2)
    # explicitly save preferences
    Prefs.savePreferences()
    foo.changes = False
    foo.close()
    IJ.run(theImp, "Add Scale Bar", s2) 
    
def flatFieldCorrectRGB(impImg, impFF, sigma=100):
    """
    flatFieldCorrectRGB(impImg, impFF, sigma=100)

    Do a flat-field (shading) correction for an RGB image

    Parameters
    ----------
    impImg: ImagePlus
        The image plus for an RGB image to correct for shading
    impFF: ImagePlus
        An even illumination image (gain) 
    sigma: number (100) px
        Blur parameter for a Gaussian blur for the gain image

    Returns
    -------
    impSc: ImagePlus
        The corrected image

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
    """
    smoothFlatField(theImp, scaFac=0.25, bShowIntermediate=False)

    Smooth a flat field correction image to generate a gain
    reference image.

    Uses ideas from: http://www.ini.uzh.ch/~acardona/fiji-tutorial/

    Parameters
    ----------
    theImp: ImagePlus
        Input image
    scaFac: float (0.25)
        Scale factor for compression
    bShowIntermediate: Boolean (False)
        Flag to show work if True
    
    Returns
    -------
    impGain: ImagePlus
        The smoothed, flat field image
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
    """
    flatField(theImp, scaFac=0.25, bShowIntermediate=False)

    Do a flat field correction by generating a gain reference image.
    Uses ideas from: http://www.ini.uzh.ch/~acardona/fiji-tutorial/

    Parameters
    ----------
    theImp: ImagePlus
        Input image
    scaFac: float (0.25)
        Scale factor for compression
    bShowIntermediate: Boolean (False)
        Flag to show work if True

    Returns
    -------
    impCor: imagePlus
        The flat field corrected image
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
    """
    median(imp, radius)

    Apply a median filter to a copy
    of the given ImagePlus, and return it.
    from: http://fiji.sc/Jython_Scripting

    Parameters
    ----------
    theImp: ImagePlus
        Input image
    radius: float
        Filter size (px)

    Returns
    -------
    copy: imagePlus
        The media-filtered image
    """
    copy = Duplicator().run(imp)
    IJ.run(copy, "Median...", "radius=" + str(radius))
    return copy
 
def removeOutliers(imp, radius, threshold, bright):
    """
    removeOutliers(imp, radius, threshold, bright)

    Apply a remove outliers filter to a copy
    of the given ImagePlus, and return it.

    from: http://fiji.sc/Jython_Scripting

    Parameters
    ----------
    imp: ImagePlus
        The input image
    radius: float
        Region of mean filter
    threshold: number
        Deviation from the median
    bright: Boolean
        if True remove thos greater than median, otherwise less.

    Returns
    -------
    copy: ImagePlus
        Corrected image
    """
    copy = Duplicator().run(imp)
    which = "Bright" if bright else "Dark"
    IJ.run(copy, "Remove Outliers...", "radius=" + str(radius) \
            + " threshold=" + str(threshold) + " which=" + which)
    return copy