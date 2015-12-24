# -*- coding: utf-8 -*-
"""
ndimage SEM image example

from here:
http://www.scipy-lectures.org/intro/scipy.html#image-processing-scipy-ndimage

1.5.11.16. Example of solution for the image processing exercise:
           unmolten grains in glass

@author: jrminter
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, misc

sizeFont=12
gitDir = os.environ['GIT_HOME']
semImgPth = gitDir + os.sep + 'OSImageAnalysis' + os.sep + 'images' + os.sep + 'scipy_ex_MV_HFV_012.jpg'
print(semImgPth)

# Open the image file MV_HFV_012.jpg and display it. Browse through
# the keyword arguments in the docstring of imshow to display the image
# with the “right” orientation (origin in the bottom left corner, and
# not the upper left corner as for standard arrays).

dat = plt.imread(semImgPth)


print(dat.shape)

# Crop the image to remove the lower panel with measure information.
cr = dat[:-60]

# Slightly filter the image with a median filter in order to refine
# its histogram. Check how the histogram changes.
filtdat = ndimage.median_filter(cr, size=(7,7))

mFig, axes = plt.subplots(ncols=3, nrows=1, figsize=(9,3))
ax0, ax1, ax2 = axes.flat 
ax0.imshow(dat, cmap=plt.cm.gray)
ax0.set_title('Original', fontsize=sizeFont)
ax0.axis('off')
ax1.imshow(cr, cmap=plt.cm.gray)
ax1.set_title('Cropped', fontsize=sizeFont)
ax1.axis('off')
ax2.imshow(filtdat, cmap=plt.cm.gray)
ax2.set_title('Filtered', fontsize=sizeFont)
ax2.axis('off')
mFig.tight_layout()
mFig.show()



hi_dat, bin_edges = np.histogram(cr, bins=np.arange(256))
hi_filtdat, bin_edges = np.histogram(filtdat, bins=np.arange(256))


fig, ax = plt.subplots()
ax.plot(bin_edges[:-1], hi_dat, linewidth=1.0, color='r', label='cropped')
ax.plot(bin_edges[:-1], hi_filtdat, linewidth=1.0, color='b', label='filtered')

legend = ax.legend(loc='upper right', shadow=True)
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
fig.show()
ax.set_xlim([0,255])
ax.set_ylim([0,40000])
fig.show()


# Using the histogram of the filtered image, determine thresholds that
# allow to define masks for sand pixels, glass pixels and bubble pixels.
# Other option (homework): write a function that determines automatically
# the thresholds from the minima of the histogram.

void = filtdat <= 50
sand = np.logical_and(filtdat > 50, filtdat <= 114)
glass = filtdat > 114

# Display an image in which the three phases are colored with three different colors.

phases = void.astype(np.int) + 2*glass.astype(np.int) + 3*sand.astype(np.int)

pFig, pAx = plt.subplots()
pAx.imshow(phases, cmap=plt.cm.Spectral)
pAx.set_title('Phases', fontsize=sizeFont)
pAx.axis('off')

# 6. Use mathematical morphology to clean the different phases.

sand_op = ndimage.binary_opening(sand, iterations=2)

# 7. Attribute labels to all bubbles and sand grains, and remove from
# the sand mask grains that are smaller than 10 pixels. To do so, use 
# ndimage.sum or np.bincount to compute the grain sizes.

sand_labels, sand_nb = ndimage.label(sand_op)
sand_areas = np.array(ndimage.sum(sand_op, sand_labels, np.arange(sand_labels.max()+1)))
mask = sand_areas > 100
remove_small_sand = mask[sand_labels.ravel()].reshape(sand_labels.shape)


# 8. Compute the mean size of bubbles.

bubbles_labels, bubbles_nb = ndimage.label(void)
bubbles_areas = np.bincount(bubbles_labels.ravel())[1:]
mean_bubble_size = bubbles_areas.mean()
median_bubble_size = np.median(bubbles_areas)
print ((mean_bubble_size, median_bubble_size))




