# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:51:56 2016

@author: jrminter
"""

import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.morphology import disk
from skimage.filters import median
from skimage.external.tifffile import imread
from skimage.filters import threshold_otsu, threshold_adaptive

gitDir = os.getenv('GIT_HOME')
relImg = '/OSImageAnalysis/images/'
imgFile = 'latex.tif'
imgPath = gitDir + relImg + imgFile

image = imread(imgPath).astype(float)

sz = 5

# med_img = median(image, disk(5))
med_img = ndi.filters.median_filter(image, size=(sz,sz))
lowpass = ndi.gaussian_filter(image, 16)

bks = med_img - lowpass
global_thresh = threshold_otsu(bks)
binary_global = bks > global_thresh

block_size = 35
binary_adaptive = threshold_adaptive(med_img, block_size, offset=10)

binary_fill = ndi.binary_fill_holes(1-binary_global).astype(int)

plt.imshow(binary_fill[400:600, 400:600]);
plt.show();