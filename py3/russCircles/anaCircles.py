"""
  anaCircles.py
  
  2013-12-14 J. R. Minter
  
  Simple particle analysis of touching circles from an image from
  John Russ.
  
  Adapted from http://pythonvision.org/basic-tutorial to python3 and
  using mainly skimage.
  
  image from http://www.reindeergraphics.com/tutorial/image-447.png.png
  
  Note that since the skimage regionprops supplies the bounding
  box, we can just eliminate the features touching the borders.

"""
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as nd

import skimage.exposure as expo
import skimage.feature as fea       # peak_local_max
import skimage.filter as fil        # rank
import skimage.io as io
import skimage.measure as mea       # regionprops
import skimage.morphology as mor    # watershed, disk


bShowIntermed = False
fOut = 'features.csv'
fImg = './circles.png'

im = io.imread(fImg)
print(im.dtype)
print(im.shape)
imgRows = im.shape[0]
imgCols = im.shape[1]

if bShowIntermed:
  io.imshow(im, cmap=plt.cm.gray)
  plt.show()

his = expo.histogram(im, nbins=256)
if bShowIntermed:
  plt.plot(his[1], his[0])
  plt.show()

thr = im > 0.5
dis = nd.distance_transform_edt(thr).astype(np.float32)
print(dis.shape)
print(dis.dtype)
if bShowIntermed:
  io.imshow(-dis, cmap=plt.cm.jet, interpolation='nearest')
  plt.show()

# denoise the EDM
blur = nd.gaussian_filter(dis,3)
if bShowIntermed:
  io.imshow(-blur, cmap=plt.cm.jet, interpolation='nearest')
  plt.show()

lMax = fea.peak_local_max(blur, indices=False, footprint=np.ones((3, 3)), labels=im)
mrk = nd.label(lMax)[0]
lab = mor.watershed(-dis, mrk, mask=thr)

props = mea.regionprops(lab, cache=True)
print("")
l = len(props)

f = open(fOut,'w')
line = "label, ecd, minor.ax.len, major.ax.len, ar"
print(line)
f.write(line+'\n')
for i in range(l):
  # check the labeled regions for border touching
  theBox = props[i].bbox
  if(theBox[0] > 0):
    if(theBox[1] > 0):
      if(theBox[2] < imgRows):
        if(theBox[3] < imgCols):
          ecd = 2.0 * math.sqrt(props[i].area/math.pi)
          ar = props[i].major_axis_length / props[i].minor_axis_length
          line = "%g, %g, %g, %g, %g" % (i+1, ecd, props[i].minor_axis_length, props[i].major_axis_length, ar )
          print(line)
          f.write(line+'\n')
          
f.close()
fig, axes = plt.subplots(ncols=3, figsize=(9, 3))
ax0, ax1, ax2 = axes
ax0.imshow(im, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('original circles')
ax1.imshow(-blur, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('blurred EDM')
ax2.imshow(lab, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('labeled circles')
for ax in axes:
  ax.axis('off')
plt.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
plt.show()





