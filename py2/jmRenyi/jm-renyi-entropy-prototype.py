# -*- coding: utf-8 -*-
"""
import os


@author: jrminter
"""

import os
from skimage.external import tifffile
from matplotlib import pyplot as plt
import numpy as np
import skimage.exposure as imexp
import jmToolsPy2

imgHom = os.getenv("IMG_ROOT")
relImg = "/key-test/ravi/"
imgDir = imgHom + relImg

os.chdir(imgDir)

def computeRenyiArrays(im):
    """computeRenyiArrays(im)
    Compute arrays required for Renyi Entropy Computations"""
    hist = imexp.histogram(im)
    bins = hist[1]
    print len(hist[0]), type(hist[0]) 
    # Convert all values to float
    hist_float = [float(i) for i in hist[0]] 
    # compute the pdf 
    pdf  = hist_float/np.sum(hist_float)
    # compute the cdf
    cumsum_pdf = np.cumsum(pdf)

    s = min(hist[1])
    e = max(hist[1])
    
    return(pdf, cumsum_pdf, s, e, bins)
    
def calcThresholdAlpha1(pdf, cumsum_pdf, s, e):
    """calcThreshold(pdf, cumsum_pdf, s, e, alpha)
    Compute the threshold for a a given alpha"""
    
    # A very small value to prevent 
    # division by zero 
    eps = np.spacing(1)

    rr = e-s
    maxlimit = len(pdf)-1
    # The second parentheses is needed because 
    # the parameters are tuples 
    h1 = np.zeros((rr,1)) 
    h2 = np.zeros((rr,1))
    # the following loop computes h1 and h2
    # values used to compute the entropy
    for ii in range(1,rr): 
        iidash = ii+s
        temp1 = (pdf[1:iidash]+eps)/(cumsum_pdf[iidash]+eps)
        h1[ii] = np.log(np.sum(temp1)+eps)
        temp2 = (pdf[iidash+1:maxlimit]+eps)/(1-cumsum_pdf[iidash]+eps)
        h2[ii] =- np.log(np.sum(temp2)+eps)

    T = h1+h2
    # Entropy value is calculated
    T = -T
    # location where the maximum entropy 
    # occurs is the threshold for the renyi entropy
    location = T.argmax(axis=0) 
    # location value is used as the threshold
    thresh = location - s
    return thresh
    
def calcThreshold(pdf, cumsum_pdf, s, e, alpha):
    """calcThreshold(pdf, cumsum_pdf, s, e, alpha)
    Compute the threshold for a a given alpha"""
    
    scalar = 1.0/(1-alpha)
    # A very small value to prevent 
    # division by zero 
    eps = np.spacing(1)

    rr = e-s
    maxlimit = len(pdf)-1
    # The second parentheses is needed because 
    # the parameters are tuples 
    h1 = np.zeros((rr,1)) 
    h2 = np.zeros((rr,1))
    # the following loop computes h1 and h2
    # values used to compute the entropy
    for ii in range(1,rr): 
        iidash = ii+s
        temp1 = np.power((pdf[1:iidash]+eps)/(cumsum_pdf[iidash]+eps),scalar)
        h1[ii] = np.log(np.sum(temp1)+eps)
        temp2 = np.power((pdf[iidash+1:maxlimit]+eps)/(1-cumsum_pdf[iidash]+eps),scalar)
        h2[ii] = np.log(np.sum(temp2)+eps)

    T = h1+h2
    # Entropy value is calculated
    T = -T*scalar
    # location where the maximum entropy 
    # occurs is the threshold for the renyi entropy
    location = T.argmax(axis=0) 
    # location value is used as the threshold
    thresh = location - s
    return thresh
    




img = tifffile.imread('ct-example.tif', key=0)

print(img.shape, img.dtype, np.amin(img), np.amax(img))


pdf, cumsum_pdf, s, e, bins = computeRenyiArrays(img)
thr = calcThreshold(pdf, cumsum_pdf, s, e, 3.0)
print("threshold alpha(3) = %.2f" % thr)
t1 = calcThresholdAlpha1(pdf, cumsum_pdf, s, e)
print("threshold alpha(1) = %.2f" % t1)

plt.plot(bins,pdf);
hFig = plt.gcf();
ax = hFig.gca();
# ax.set_ylim(0,50000)
ax.set_yscale('log');
# ax.axvline(x=thresh,linewidth=2, color='r');
hFig.show();
# plt.show()





