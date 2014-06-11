"""
jmHyperSpy: Convenience functions for working with HyperSpy
==============================================================

The :mod:`~jmHyperSpy` module is imported for use by:

  import jmHyperSpy as jmh
  
Ver    Date      Who  Comments
===  ==========  ===  =================================================
0.1  2014-06-10  JRM  Initial prototype
0.2  2014-06-11  JRM  Added functions plotEdsSpc, makeEdsMaxPxSpc, and 
                      makeEdsSumSpc.
"""
# -*- coding: utf-8 -*-

# get the key imports
import os
import os.path
from StringIO import StringIO
import hyperspy.hspy as hs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython import display, core
from IPython.core.pylabtools import *

def plotEdsSpc(ss, logY=True, crL=22, crR=2):
  """plotEdsSpc(ss, logY=True, crL=22, crR=2)
  Plot a sum spectrum or  max pixel from an EDS spectrum image
  
  Parameters
  ----------
  ss    : spectrum   A hyperspy EDS sum spectrum returned from makeEdsSumSpc
                     or a max pixel spectrum from makeEdsMaxPxSpc
  logY  : boolean    Plot y axis as log. Default is True.
  crL   : int        Crop channels from the left. Default is 22.
  crR   : int        Crop channels from the right. Default is 2.
  
  Returns
  -------
  A matplotlib plot
  """
  gain = ss.axes_manager[0].scale
  off = ss.axes_manager[0].offset
  y = ss.data
  l = y.shape[0]
  x = gain*(np.arange(l).astype(float))+off
  x = x[crL:l-1-crR]
  y = y[crL:l-1-crR]
  plt.plot(x,y)
  plt.xscale('linear', nonposx='mask')
  if logY:
    plt.yscale('log', nonposy='mask')
  else:
    plt.yscale('linear', nonposy='mask')
  plt.xlabel('keV')
  plt.ylabel('counts')
  plt.title(ss.metadata.General.title)
  
def makeEdsMaxPxSpc(si, edsEvCh, edsZeOf, npChan=0):
  """makeEdsMaxPxSpc(si, edsEvCh, edsZeOf, npChan=0)
  Make a maximum pixel spectrum from an EDS spectrum image
  
  Parameters
  ----------
  si      : spectrum image  A hyperspy spectrum image
  edsEvCh : float           The eV per channel for the detector.
                            will be converted to keV internally.
  edsZeOf : float           The zero offset for the detector in eV
                            Will be converted to keV internally.
  npChan  : int             Number of channels to set to zero for
                            the noise peak. Defaults to zero. 
  Returns
  -------
  A hyperspy EDS spectrum
  
  Note: one can get the parameters for a DTSA-II detector easily from 
  the command line.
  
  1> listDetectors()
  ...
  d2  Oxford p4 05eV 2K
  ...
  2>  d2.getChannelWidth()
  4.9943077562795395
  3>  d2.getZeroOffset()
  -94.48424156889702
  """
  spc = si.to_spectrum()
  dat = spc.data
  dat = dat.astype(float)
  print dat.shape
  y = np.arange(dat.shape[2]).astype(float)
  for k in range(dat.shape[2]):
    a = dat[:, :, k]
    maxV = float(np.amax(a))
    y[k] = maxV
  lV = min(y)
  for i in range(npChan):
    y[i] = lV
  s = hs.signals.Spectrum(y)
  # Define the axis properties
  s.axes_manager.signal_axes[0].name = 'Energy'
  s.axes_manager.signal_axes[0].units = 'keV'
  s.axes_manager.signal_axes[0].scale = edsEvCh/1000.
  s.axes_manager.signal_axes[0].offset = edsZeOf/1000.
  caption = "%s Max Pix Spectrum" % si.metadata.General.title
  s.metadata.General.title = caption
  s.metadata.Signal.signal_origin = si.metadata.Signal.signal_origin
  s.metadata.Signal.signal_type = si.metadata.Signal.signal_type
  return(s)

def makeEdsSumSpc(si, edsEvCh, edsZeOf, npChan=0):
  """makeEdsSumSpc(si, edsEvCh, edsZeOf, npChan=0)
  Make a sum spectrum from an EDS spectrum image
  
  Parameters
  ----------
  si      : spectrum image  A hyperspy spectrum image
  edsEvCh : float           The eV per channel for the detector.
                            will be converted to keV internally.
  edsZeOf : float           The zero offset for the detector in eV
                            Will be converted to keV internally.
  npChan  : int             Number of channels to set to zero for
                            the noise peak. Defaults to zero. 
  Returns
  -------
  A hyperspy EDS spectrum
  
  Note: one can get the parameters for a DTSA-II detector easily from 
  the command line.
  
  1> listDetectors()
  ...
  d2  Oxford p4 05eV 2K
  ...
  2>  d2.getChannelWidth()
  4.9943077562795395
  3>  d2.getZeroOffset()
  -94.48424156889702
  """
  spc = si.to_spectrum()
  dat = spc.data
  dat = dat.astype(float)
  print dat.shape
  sl1 = dat.sum(axis=0)
  print sl1.shape # (256, 1024)
  sl2 = sl1.sum(axis=0)
  print sl2.shape # (1024,)
  lV = min(sl2)
  for i in range(npChan):
    sl2[i] = lV
  s = hs.signals.Spectrum(sl2)
  # Define the axis properties
  s.axes_manager.signal_axes[0].name = 'Energy'
  s.axes_manager.signal_axes[0].units = 'keV'
  s.axes_manager.signal_axes[0].scale = edsEvCh/1000.
  s.axes_manager.signal_axes[0].offset = edsZeOf/1000.
  caption = "%s Sum Spectrum" % si.metadata.General.title
  s.metadata.General.title = caption
  s.metadata.Signal.signal_origin = si.metadata.Signal.signal_origin
  s.metadata.Signal.signal_type = si.metadata.Signal.signal_type
  return(s)
  

  

def makeAvgSlice(ar, begin, end):
  """makeAvgSlice(ar, begin, end)
  Make an average slice image from a 3-d data cube array
  Parameters
  ----------
  ar    : array  a 3-d numpy array from hyperspy
  begin : int    beginning channel to average (zero based)
  end   : int    ending channel

  Returns
  -------
  Numpy array with averaged slice
  """
  x = ar.copy()
  x = x.astype(float)  
  h = x.shape[0]
  w = x.shape[1]
  d = x.shape[2]
  if (end > d-1):
    end = d-1
  delta = float(end) - float(begin)
  sl = x[0:h-1,0:w-1,begin:end]
  bl = sl.sum(axis=2)/delta
  return(bl)

def cropSlice(sl, t, b, l, r):
  """cropSlice(sl, t, b, l, r)
  Crop the input slice to remove blank info
  
  Parameters
  ----------
  sl  : array  a 3-d numpy array from hyperspy
  t   : int    number of channels to crop from top
  b   : int    number of channels to crop from bottom
  l   : int    number of channels to crop from left
  l   : int    number of channels to crop from right

  Returns
  -------
  Numpy array with averaged slice
  """
  h = sl.shape[0]
  w = sl.shape[1]
  print(h)
  print(w)
  cr = sl[t:h-b-1,l:w-r-1]
  print(t)
  print(b)
  return(cr)
  
def makeBksAvgSlice(ar, elRange, bkgRange1, bkgRange2=None):
  """makeBksAvgSlice(ar, elRange, bkgRange1, bkgRange2=None)
  Make a background-subtracted averaged slice from a 3-d data-cube
  for specified element and background ranges.
  
  Parameters
  ----------
  ar        : array  a 3-d numpy array from hyperspy
  elRange   : int list [start, end] channel for element
  bkgRange1 : int list [start, end] channel for bkg region 1
  bkgRange2 : int list [start, end] channel for bkg region 2
              Defaults to 'none'
  Returns
  -------
  Numpy array with averaged slice for the element
  """
  el = makeAvgSlice(ar, elRange[0], elRange[1])
  delta = float(elRange[1]) - float(elRange[0])
  if (bkgRange2==None):
    bkg =  makeAvgSlice(ar, bkgRange1[0], bkgRange1[1])
    bks = el - bkg
    bks = delta * bks
    bks = bks.clip(0)
    return(bks)
  else:
    bkg1 = makeAvgSlice(ar, bkgRange1[0], bkgRange1[1])
    bkg2 = makeAvgSlice(ar, bkgRange2[0], bkgRange2[1])
    bkg = 0.5*(bkg1+bkg2)
    bks = el - bkg
    bks = delta * bks
    bks = bks.clip(0)
    return(bks)
    
def plotSlice(sl, title, umPerPx, xinch = 9.0):
  """ plotSlice(sl, title, umPerPx)
  Make a matplotlib plot of a slice with a title and a
  gray color bar. The full width of the image is appended
  to the title.
  
  Parameters
  ----------
  sl        : array  a 2-d numpy array to plot
  title     : string A base title for the plot
  umPerPx   : float  The scale in microns/px for the data
  xinch     : float The width of the figure (in)
              Defaults to 9.0
  Returns
  -------
  Numpy array with averaged slice for the element
  """
  h, w = sl.shape
  aspR = float(h)/float(w)
  scale = umPerPx * float(w)
  yinch = aspR * xinch
  # plot and save in the same size as the original
  plt.figure(figsize=(xinch,yinch))
  caption = "%s (w = %.1f $\mu$ m)" % (title, scale)
  plt.imshow(sl)
  plt.title(caption)
  plt.axis('off')
  plt.colorbar()
  plt.show()

def fixIncaRpl(path):
  """correct_INCA_format(path)
  Updates the Inca .rpl file to the new Lispix format
    Parameters
  ----------
  path: a string with the path to the file
  """
  fp = open(path, "r+")
  fp_list = list()
  fp.seek(0)
  if '(' in fp.readline():
    for line in fp:
      line = line.replace(
        "(MLX::",
        "").replace(
        " : ",
        "\t").replace(
        " :",
        "\t").replace(
        " ",
        "\t").lower().strip().replace(
        ")",
        "\n")
      if "record-by" in line:
        if "image" in line:
          line = "record-by\timage"
        if "vector" in line:
          line = "record-by\tvector"
        if "dont-care" in line:
          line = "record-by\tdont-care"
      fp_list.append(line)
    fp.close()
    fp = open(path, "w")
    fp.write("key\tvalue\n");
    fp.writelines(fp_list)
  fp.seek(0)
  fp.close()
  return