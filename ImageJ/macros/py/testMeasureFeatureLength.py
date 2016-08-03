# testMeasureFeatureLength.py
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from math import sqrt
from java.awt import Color, Font
from ij import IJ, ImagePlus, WindowManager, Prefs, ImageStack
from ij.gui import Roi, TextRoi, ImageRoi, Overlay, ImageCanvas
from ij.gui import ShapeRoi, PointRoi

import jmFijiGen as jmg

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

    Version of 2016-08-03

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
                length = round(length, 3)
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
                            f=open(csvPath, 'a')
                        else:
                            f=open(csvPath, 'w')
                            strLine = 'img, length (%s)\n' % unit
                            f.write(strLine)
                    else:
                        f=open(csvPath, 'w')
                        strLine = 'img, length (%s)\n' % unit
                        f.write(strLine)
                    strLine = "%s, %.6f\n" % (imp.getShortTitle(), length)
                    f.write(strLine)
                    f.close()
                strMsg = "measured %s" % imp.getShortTitle()
                print(strMsg)

            else:
                print("You need a line ROI")

            # finally deselect
            IJ.run("Select None")


imp = IJ.getImage()
jmg.measureFeatureLength(imp, lw = 2,
                         csvPath='C:/Users/l837410/Desktop/foo.csv',
                         bAppend=True,
                         offset = -30, digits = 3,
                         font = 18, linCol = Color.YELLOW,
                         labCol = Color.WHITE,
                         bDebug = False)