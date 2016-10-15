# -*- coding: utf-8 -*-
"""
makeOxfordAZtecIni.py

A script to write metadata for an AZtec image to an ini file

Modifications
  Date      Who  Ver                       What
----------  ---  ------  -------------------------------------------------
2016-10-15  JRM 0.5.00  First port to pure python. Had trouble with the
                        ImageJ scijava libs handling script parameters.
                        Was REALLY annoying. This uses TKInter. Not the
                        nicest GUI but seems to work right. Also it uses
                        ab .ini file NOT the Windows registry...

"""

__revision__ = "$Id: makeOxfordAZtecIni.py John R. Minter $"
__version__ = "0.5.00"

from tkinter import *
from tkinter import filedialog as fd
import sys
import string
import math
import os
import configparser

def computeTiltScaleFactorY(fScaleX, tiltDeg):
    """computeTiltScaleFactorY(fScaleX, tiltDeg)
       Compute the fore-shortened Y-axis scale factor given the
       X-axis scale factor and tilt angle [deg]
    """
    # convert to radians and compute cos
    factor = math.cos(tiltDeg*math.pi/180.0)
    fScaleY = fScaleX/factor
    return fScaleY

def estimateAztecScaleFactorX(mag, scanWidthPx=1024,
                              slope=289251.80, slopeSE=16.54,
                              rDigits=7):
    """estimateAztecScaleFactorX(mag, scanWidthPx=1024,
                                 slope=289251.80, slopeSE=16.54,
                                 rDigits=7)
                                 
    Estimate the scale factor [microns/px] from a linear fit of the
    image full width as a function of the inverse magnification.
    
    Parameters
    ----------
    mag: number
        The SEM magnification
    scanWidthPx: number (1024)
        The full width of the image scan in pixels. The maximum is 4096
    slope: number (289251.80)
         The slope of the inverse magnification plot. Note the intercept
         is constrained to zero.
    slopeSE: number (16.54)
         The standard error of the fit
    rDigits: integer (5)
        Number of digits to round the microns/pix

    Returns
    -------
    sf: list [mean, LCL, UCL]
    The scale factor in microns per pixel. The first value is the mean.
    The second and third values are the lower and upper confidence
    intervals.
    """
    imFWMu  = slope/mag
    imFWLCL = (slope-slopeSE)/mag
    imFWUCL = (slope+slopeSE)/mag
    sfMu = round(imFWMu/scanWidthPx, rDigits)
    sfLC = round(imFWLCL/scanWidthPx, rDigits)
    sfUC = round(imFWUCL/scanWidthPx, rDigits)
    sf = [sfMu, sfLC, sfUC]
    return sf


class App:
    def __init__(self,parent):
        # define the variables
        self.mIniFile = StringVar()
        self.mDetector = StringVar()
        self.mScan = StringVar()
        self.mComment = StringVar()
        self.mBaseName = StringVar()
        self.mMessage = StringVar()
        # really booleans
        self.mAppend = IntVar()
        self.mFIB = IntVar()
        # integers
        self.mImgWidth = IntVar()
        self.mSpot = IntVar()
        # doubles
        self.mWD = DoubleVar()
        self.mTilt = DoubleVar()
        self.mkV = DoubleVar()
        self.mMag = DoubleVar()


        f = Frame(parent)
        f.pack(padx=15,pady=15)
        self.lab0 = Label(f, text='Ini File')
        self.lab0.pack(side = TOP, pady=1)
        self.IniFileBox = Entry(f,textvariable=self.mIniFile, width=80)
        self.IniFileBox.pack(side= TOP,padx=10,pady=2)
        
        self.mAppend.set(0)
        self.IniAppend = Checkbutton(f, text="append", variable=self.mAppend)
        self.IniAppend.pack(side= TOP,padx=10,pady=2)
        
        self.mFIB.set(0)
        self.FIB = Checkbutton(f, text="FIB", variable=self.mFIB)
        self.FIB.pack(side= TOP,padx=10,pady=2)
        
        self.lab1= Label(f, text='Image Width')
        self.lab1.pack(side = TOP, pady=1)
        self.ImgWidthBox = Entry(f,textvariable=self.mImgWidth, width=8)
        self.ImgWidthBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab2= Label(f, text='e0 [kV]')
        self.lab2.pack(side = TOP, pady=1)
        self.kVBox = Entry(f,textvariable=self.mkV, width=8)
        self.kVBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab3= Label(f, text='Spot Size')
        self.lab3.pack(side = TOP, pady=1)
        self.SpotBox = Entry(f,textvariable=self.mSpot, width=3)
        self.SpotBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab4 = Label(f, text='Working Distance [mm]')
        self.lab4.pack(side = TOP, pady=1)
        self.WDBox = Entry(f,textvariable=self.mWD, width=6)
        self.WDBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab5 = Label(f, text='Tilt Angle [deg]')
        self.lab5.pack(side = TOP, pady=1)
        self.TiltBox = Entry(f,textvariable=self.mTilt, width=6)
        self.TiltBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab6 = Label(f, text='Detector')
        self.lab6.pack(side = TOP, pady=1)
        self.DetBox = Entry(f,textvariable=self.mDetector, width=16)
        self.DetBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab7 = Label(f, text='Scan')
        self.lab7.pack(side = TOP, pady=1)
        self.ScanBox = Entry(f,textvariable=self.mScan, width=16)
        self.ScanBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab8 = Label(f, text='Other Comment')
        self.lab8.pack(side = TOP, pady=1)
        self.ComBox = Entry(f,textvariable=self.mComment, width=60)
        self.ComBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab9 = Label(f, text='Base Image Name')
        self.lab9.pack(side = TOP, pady=1)
        self.NameBox = Entry(f,textvariable=self.mBaseName, width=40)
        self.NameBox.pack(side= TOP,padx=10,pady=2)
        
        self.lab10 = Label(f, text='Magnification [X]')
        self.lab10.pack(side = TOP, pady=1)
        self.NameBox = Entry(f,textvariable=self.mMag, width=16)
        self.NameBox.pack(side= TOP,padx=10,pady=2)
        
        # message box
        self.lab11 = Label(f, text='')
        self.lab11.pack(side = TOP, pady=1)
        self.lab12 = Label(f, text='Messages')
        self.lab12.pack(side = TOP, pady=2)
        self.MessageBox = Entry(f,textvariable=self.mMessage, width=80)
        self.MessageBox.pack(side= TOP,padx=10,pady=2)
        
        # pull in last data
        self.read_file()
        self.mMessage.set("Message")
        
        self.button = Button(f, text="read file",command=self.read_file)
        self.button.pack(side=LEFT,padx=2,pady=10)
        
        # self.exit = Button(f, text="exit", command=f.quit)
        # self.exit.pack(side=LEFT,padx=2,pady=10)
        
        self.button = Button(f, text="write to ini",command=self.write_file)
        self.button.pack(side=RIGHT,padx=2,pady=10)
        
    def write_file(self):
        if self.mAppend:
            f = open(self.mIniFile.get(), 'a')
        else:
            f = open(self.mIniFile.get(), 'w')
        f.write("[" + self.mBaseName.get() + "]\n")
        strLine = "Mag=%.1f" % self.mMag.get() + "\n"
        f.write(strLine)
        fScale = estimateAztecScaleFactorX(self.mMag.get(),
                                           self.mImgWidth.get(),
                                           289251.80, 16.54, 7)
        fScaleX = fScale[0]
        strLine = "ScaleX=%.6f" %  fScaleX + "\n"
        f.write(strLine)
        if self.mFIB.get() > 0:
            tiltDeg = 90.0 - self.mTilt.get()
        else:
            tiltDeg = self.mTilt.get()
        fScaleY = computeTiltScaleFactorY(fScaleX, tiltDeg)
        strLine = "ScaleY=%.6f" %  fScaleY + "\n"
        f.write(strLine)
        strLine = "Units=µm\n"
        f.write(strLine)
        fmt = "Comment=%g kV, S%d, %.1f mm, %s, %.1f deg tilt, %s, %s\n\n"
        strLine = fmt % (self.mkV.get(), self.mSpot.get(),
                         self.mWD.get(), self.mDetector.get(),
                         self.mTilt.get(), self.mScan.get(),
                         self.mComment.get())
        f.write(strLine)
        f.close()

        fmt = "Proc image %s at magn %.1fX"
        strMsg = fmt % (self.mBaseName.get(), self.mMag.get())
        self.mMessage.set(strMsg)
        self.write_ini()
        

    def write_ini(self):
        config = configparser.ConfigParser()
        config['LAST'] = {}
        config['LAST']['ini'] = self.mIniFile.get()
        config['LAST']['append'] = "%d" % self.mAppend.get()
        config['LAST']['fib'] = "%d" % self.mFIB.get()
        config['LAST']['width'] = "%d" % self.mImgWidth.get()
        config['LAST']['e0'] = "%.1f" % self.mkV.get()
        config['LAST']['spot'] = "%d" % self.mSpot.get()
        config['LAST']['wd'] = "%.1f" % self.mWD.get()
        config['LAST']['tilt'] = "%.1f" % self.mTilt.get()
        config['LAST']['det'] = "%s" % self.mDetector.get()
        config['LAST']['scan'] = "%s" % self.mScan.get()
        config['LAST']['other'] = "%s" % self.mComment.get()
        config['LAST']['basename'] = "%s" % self.mBaseName.get()
        config['LAST']['mag'] = "%.1f" % self.mMag.get()
        
        strFile = '/data/AZtec/last.ini'
        with open(strFile, 'w') as configfile:
            config.write(configfile)

        fmt = "Proc img %s at magn %.1f X and update ini"
        strMsg = fmt % (self.mBaseName.get(), self.mMag.get())
        self.mMessage.set(strMsg)
        return
        
    def read_file(self):
        strFile = '/data/AZtec/last.ini'
        config = configparser.ConfigParser()
        config.read(strFile)
        self.mIniFile.set(config['LAST']['ini'])
        self.mAppend.set(int(config['LAST']['append']))
        self.mFIB.set(config['LAST']['fib'])
        self.mImgWidth.set(config['LAST']['width'])
        self.mkV.set(config['LAST']['e0'])
        self.mSpot.set(config['LAST']['spot'])
        self.mWD.set(config['LAST']['wd'])
        self.mTilt.set(config['LAST']['tilt'])
        self.mDetector.set(config['LAST']['det'])
        self.mScan.set(config['LAST']['scan'])
        self.mComment.set(config['LAST']['other'])
        self.mBaseName.set(config['LAST']['basename'])
        self.mMag.set(config['LAST']['mag'])
        return



root = Tk()
root.title('makeOxfordAZtecIni.py v. 0.5.00')
app = App(root)

root.mainloop()