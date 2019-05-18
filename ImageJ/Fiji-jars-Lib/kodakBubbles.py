from __future__ import division
# -*- coding: utf-8 -*-

"""
kodakBubbles.py

Place a copy of this file in the C:\Apps\Fiji.app.win32\jars\Lib dir

    Modifications

   Date     Who   Ver                      What
----------  ---  ------  ---------------------------------------------
2017-10-05  JRM  1.0.90  First prototype
2017-10-10  JRM  1.1.00  First test release
2017-10-19  JRM  1.1.10  Keep  kodakBubbles.py under VC in Nair project
"""


__revision__ = "$Id: kodakBubbles.py John R. Minter Modified 2017-10-19$"
__version__ = "1.1.10"

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

def loadBubbleImage(path, scale=0.7326, unit="um",
                    radius=2, saturated=0.005):
    """loadBubbleImage

    Load and pre-process a bubble image. It loads the image, removes
    noise and scales the intensity.

    Parameters
    ----------
    path: string
        The path to the desired image file
    scale: number (0.735)
        The scale of the images in microns/px
    unit: string ("um")
        The units for the X- and Y-scale
    radius: number (2)
        The radius for a median filter
    saturated: number (0.005)
        The percentage of the intensity on the ends

    Returns
    -------
    imp: ImagePlus
        The scaled image. Does not immediately display for headless
        operation

    Example
    -------

    import kodakBubbles as bub

    path = "C:/Data/images/Lobo-bubbles/Set1/Image1.jpg"
    imp = bub.loadBubbleImage(path)

    """
    imp = IJ.openImage(path)
    ti = imp.getTitle()
    cal = imp.getCalibration()
    cal.pixelWidth = scale
    cal.pixelHeight = scale
    cal.pixelDepth = scale
    cal.setUnit(unit)
    IJ.run(imp, "16-bit", "")
    strTwo = "radius=%d" % (radius)
    IJ.run(imp, "Median...", strTwo)
    strTwo = "saturated=%.3f" % (saturated)
    IJ.run(imp, "Enhance Contrast", strTwo)
    IJ.run(imp, "8-bit", "")
    return(imp)


def binarizeBubbleImage(imp, atrFrom=211, atrThen=5):
    """binarizeBubbleImage(imp, atrFrom=211, atrThen=5)

    Make a binary image of the bubbles ready for segmentation

    Parameters
    ----------

    imp: ImagePlus
        The input image

    atrFrom: integer (211)
        The first parameter for the adaptive threshold. A size.

    atrThen: integer (5)
        An offset

    Returns
    -------
    imp: ImagePlus
        The binary image. Does not immediately display for headless
        operation

    Example
    -------

    import kodakBubbles as bub

    imp = bub.binarizeBubbleImage(imp, atrFrom=211, atrThen=5)

    """
    name = imp.getShortTitle() + '-ws'
    wrk = imp.duplicate()
    strTwo = "using=[Weighted mean] from=%d then=%d" % (atrFrom, atrThen)
    IJ.run(wrk, "adaptiveThr ", strTwo);
    blackBackground = True
    IJ.run(wrk, "Make Binary", "")
    IJ.run(wrk, "Fill Holes", "")
    IJ.run(wrk, "Watershed", "")
    wrk.setTitle(name)
    return(wrk)

def detectBubbles(imp, minAreaPx=20, circMin=0.8):
    """detectBubbles(imp, minAreaPx=20, circMin=0.8)

    detect bubbles in a binary image

    Parameters
    ----------

    imp: ImagePlus
        The input image

    minAreaPx: number (20)
        The minimum area in pixels for a feature to be treated as a
        bubble

    circMin: number (0.80)
        The minimum circularity for a feature to be a properly
        detected bubble

    Returns
    -------
    imp: ImagePlus
        The segmented image

    Example
    -------

    import kodakBubbles as bub

    imp = bub.detectBubbles(imp, minAreaPx=20, circMin=0.8)

    """
    wrk = imp.duplicate()
    name = imp.getShortTitle() + '-ana'
    cal = wrk.getCalibration()
    scale = cal.pixelWidth
    minAreaSqUm = minAreaPx*scale
    strTwo  = "area center fit shape limit display "
    strTwo += "redirect=None decimal=3"  
    IJ.run(wrk, "Set Measurements...", strTwo)

    strTwo += "size=%f-Infinity " % (minAreaSqUm)
    strTwo += "circularity=%f-1.00 " % (circMin)
    strTwo += "show=Outlines display add" 
    IJ.run(wrk, "Analyze Particles...", strTwo)
    wrk.setTitle(name)
    return(wrk)


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

    Example
    -------

    import kodakBubbles as bub

    imp = bub.watershedBinaryImage(imp)

    """
    wrk = imp.duplicate()
    cal = wrk.getCalibration()
    wat = wrk.createImagePlus()
    ip = wrk.getProcessor().duplicate()
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
    anaCircParticles(imp, wat, csvPath, minArea=10, maxArea=100000, 
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


    imp = bub.anaCircParticles(imp, wat, csvPath,
                               minArea=10, maxArea=100000, 
                               minCirc=0.35, maxAR=1.05, imgNo=1,
                               labFont=20, colOut=Color.red,
                               colLab=Color.black,
                               bAppend=False, bVerbose=False)

    """
    jFont = Font("SanSerif", Font.BOLD, labFont)
    cal = imp.getCalibration()
    out = imp.createImagePlus()
    ip = imp.getProcessor().duplicate().convertToByteProcessor()
    name = imp.getShortTitle() + '-meas'
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
        ar = lAR[i]
        xM = lXm[i]
        yM = lYm[i]
        ecd = 2.0 * math.sqrt(area/math.pi)
        if circ >= minCirc:
            if ar <= maxAR:
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

    # print(len(partID), len(partAR))

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

    win = WindowManager.getWindow("Results")
    win.close(False)

    return out

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
