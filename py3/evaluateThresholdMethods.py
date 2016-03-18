# -*- coding: utf-8 -*-
"""
evaluateThresholdMethods.py

Test the skimage threshold methods on a desired image

Created on Mon Dec 28 22:51:48 2015

@author: jrminter
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, io, filters, transform

def displayImg(img, name='image', fSize=12):
    iFig, axes = plt.subplots(ncols=1, nrows=1, figsize=(5,5))
    ax0 = axes #.flat 
    ax0.imshow(img, cmap=plt.cm.gray)
    ax0.set_title(name, fontsize=fSize)
    ax0.axis('off')
    iFig.tight_layout();
    iFig.show();
    return(iFig)
    
def displayAll(ld, ln, fSize=12):
    iPan, axes = plt.subplots(ncols=3, nrows=2, figsize=(15,10))
    for i, ax in enumerate(axes.flat, start=0):
        ax.imshow(ld[i], cmap=plt.cm.gray)
        ax.set_title(ln[i], fontsize=fSize)
        ax.axis('off')
    iPan.tight_layout();
    iPan.show();
    return(iPan)

gitHome = os.getenv('GIT_HOME')
imRel = '/OSImageAnalysis/images/blobs.gif'
fi = gitHome + imRel

print(fi)

im =io.imread(fi)


print(im.shape, im.dtype)

binThrAd = filters.threshold_adaptive(im,21, method='median', offset=0, mode='reflect', param=None)

thrIso = filters.threshold_isodata(im, nbins=256, return_all=False)
binIso = im > thrIso
tiIso = "Iso %d" % thrIso
print(thrIso)

thrLi = filters.threshold_li(im)
binLi = im > thrLi
tiLi = "Li %d" % thrLi

thrOtsu = filters.threshold_otsu(im, nbins=256)
binOtsu = im > thrOtsu
tiOtsu = "Otsu %d" % thrOtsu

thrYen = filters.threshold_yen(im, nbins=256)
binYen = im > thrYen
tiYen = "Yen %d" % thrYen

# cImg = displayImg(binYen, name='coins-binYen')
# cImg.show()

fPan = displayAll([im, binThrAd, binIso, binLi, binOtsu, binYen], ["Original", "Adaptive", tiIso, tiLi, tiOtsu, tiYen], fSize=12)
fPan.show()



