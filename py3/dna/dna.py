"""
  dna.py
  
  2013-12-14 J. R. Minter
  
  Simple particle analysis of nuclei imaged by fluorescence imaging
  of DNA.
  
  Adapted from http://pythonvision.org/basic-tutorial to python3 and
  using mainly skimage.
  
  image from http://pythonvision.org/media/files/images/dna.jpeg
  
  Note that since the skimage regionprops supplies the bounding
  box, we can just eliminate the features touching the borders.

  2015-11-30  JRM  Updated skimage.filter to skimage.filters
  
  

"""
import math
import numpy as np
import skimage.io as io
import skimage.feature as fea       # peak_local_max
import skimage.segmentation as seg  # find_boundaries, visualize_boundaries
import skimage.morphology as mor    # watershed, disk
import skimage.filters as fil        # threshold_otsu
import skimage.measure as mea       # regionprops
import scipy
import scipy.ndimage as nd
import matplotlib.pyplot as plt
import pymorph as pm
import mahotas as mh

bShowIntermed = False

fOut = 'features.csv'
fImg = 'dna.jpeg'

dna = io.imread(fImg)

if bShowIntermed:
  plt.imshow(dna)
  plt.gray()
  plt.show()

print(dna.shape)

imgRows = dna.shape[0]
imgCols = dna.shape[1]
print(dna.dtype)
print(dna.max())
print(dna.min())

# T = mh.thresholding.otsu(dna)
T = fil.threshold_otsu(dna)

dnaf = nd.gaussian_filter(dna, 16)
thr = dnaf > T

if bShowIntermed:
  plt.imshow(thr)
  plt.show()

dis = nd.distance_transform_edt(thr).astype(np.float32)
if bShowIntermed:
  print(dis.shape)
  print(dis.dtype)
  plt.imshow(-dis, cmap=plt.cm.jet, interpolation='nearest')
  plt.show()

# denoise the EDM
blur = nd.gaussian_filter(dis, 5)
if bShowIntermed:
  plt.imshow(-blur, cmap=plt.cm.jet, interpolation='nearest')
  plt.show()

# rmax = pm.regmax(dnaf)
rmax = fea.peak_local_max(blur, indices=False, footprint=np.ones((3, 3)))

if bShowIntermed:
  print(rmax.shape)
  print(rmax.dtype)
  print(rmax.max())
  print(rmax.min())
  plt.imshow(pm.overlay(dna, rmax))
  plt.show()

mrk = nd.label(rmax)[0]
lab = mor.watershed(-blur, mrk, mask=thr)

props = mea.regionprops(lab, intensity_image=dna, cache=True)

print("")
l = len(props)

f = open(fOut,'w')
line = "label, ecd, minor.ax.len, major.ax.len, ar, solidity"
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
          line = "%g, %g, %g, %g, %g, %g" % (i+1, ecd, props[i].minor_axis_length, props[i].major_axis_length, ar, props[i].solidity)
          print(line)
          f.write(line+'\n')
          
f.close()
fig, axes = plt.subplots(ncols=3, figsize=(9, 3))
ax0, ax1, ax2 = axes
ax0.imshow(dna, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('original dna')
ax1.imshow(-blur, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('blurred EDM')
ax2.imshow(lab, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('labeled dna')
for ax in axes:
  ax.axis('off')
plt.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
plt.show()

