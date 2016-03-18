# -*- coding: utf-8 -*-
"""
analyzeCoins.py

This analysis is adapted from Figure 1 of Van der Walt et al.,
scikit-image: image processing in Python,  PeerJ,
DOI 10.7717/peerj.453 (2014)

This version was adapted by J. R. Minter on 2015-12-23 to change to 
match the scikit-image package changes in version 0.11.3 under
Anaconda 2.4.1 with Python 3.5.1
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage import data, io, filters
from skimage.feature import peak_local_max, canny
from skimage.measure import regionprops, label


sizeFont = 18

image = data.coins() # or any NumPy array!
edges = filters.sobel(image)
io.imshow(edges);

# Load a small section of the image.
image = data.coins()[0:95, 70:370]

fig, axes = plt.subplots(ncols=2, nrows=3, figsize=(8, 4))
ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat
ax0.imshow(image, cmap=plt.cm.gray)
ax0.set_title('Original', fontsize=sizeFont)
ax0.axis('off')

# Histogram.
values, bins = np.histogram(image, bins=np.arange(256))
ax1.plot(bins[:-1], values, lw=2, c='k')
ax1.set_xlim(xmax=256)
ax1.set_yticks([0, 400])
ax1.set_aspect(.2)
ax1.set_title('Histogram', fontsize=sizeFont)

# Apply threshold.
bw = filters.threshold_adaptive(image, 95, offset=-15)
ax2.imshow(bw, cmap=plt.cm.gray)
ax2.set_title('Adaptive threshold', fontsize=sizeFont)
ax2.axis('off')

# Find maxima
coordinates = peak_local_max(image, min_distance=20)

ax3.imshow(image, cmap=plt.cm.gray)
ax3.autoscale(False)
ax3.scatter(coordinates[:, 1], coordinates[:, 0],  marker='.', color='r')
ax3.set_title('Peak local maxima', fontsize=sizeFont)
ax3.axis('off')

# Detect edges.
edges = canny(image, sigma=3, low_threshold=10, high_threshold=80)
ax4.imshow(edges, cmap=plt.cm.gray)
ax4.set_title('Edges', fontsize=sizeFont)
ax4.axis('off')

# Label image regions.
label_image = label(edges)

ax5.imshow(image, cmap=plt.cm.gray)
ax5.set_title('Labeled items', fontsize=sizeFont)
ax5.axis('off')

for region in regionprops(label_image):
    # Draw rectangle around segmented coins.
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
    ax5.add_patch(rect)


plt.tight_layout();
plt.show();
