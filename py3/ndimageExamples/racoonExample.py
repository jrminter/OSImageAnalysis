# -*- coding: utf-8 -*-
"""
racoon ndimage example

from here:
http://www.scipy-lectures.org/intro/scipy.html#image-processing-scipy-ndimage

@author: jrminter
"""
# import os
# import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, misc


sizeFont=12

face = misc.face(gray=True)
shifted_face = ndimage.shift(face, (50, 50))
shifted_face2 = ndimage.shift(face, (50, 50), mode='nearest')
rotated_face = ndimage.rotate(face, 30)
cropped_face = face[50:-50, 50:-50]
zoomed_face = ndimage.zoom(face, 2)
zoomed_face.shape

fig, axes = plt.subplots(ncols=6, nrows=1, figsize=(24,3))
ax0, ax1, ax2, ax3, ax4, ax5  = axes.flat 
ax0.imshow(face, cmap=plt.cm.gray)
ax0.set_title('Original', fontsize=sizeFont)
ax0.axis('off')
ax1.imshow(shifted_face, cmap=plt.cm.gray)
ax1.set_title('Shift 1', fontsize=sizeFont)
ax1.axis('off')
ax2.imshow(shifted_face2, cmap=plt.cm.gray)
ax2.set_title('Shift 2', fontsize=sizeFont)
ax2.axis('off')
ax3.imshow(rotated_face, cmap=plt.cm.gray)
ax3.set_title('Rotated', fontsize=sizeFont)
ax3.axis('off')
ax4.imshow(cropped_face, cmap=plt.cm.gray)
ax4.set_title('Crop', fontsize=sizeFont)
ax4.axis('off')
ax5.imshow(zoomed_face, cmap=plt.cm.gray)
ax5.set_title('Zoom', fontsize=sizeFont)           
ax5.axis('off')
fig.tight_layout()
fig.show()




