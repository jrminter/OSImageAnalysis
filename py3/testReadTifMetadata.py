# -*- coding: utf-8 -*-
"""
testReadTifMetadata.py

Read the metadata from an FEI FIB 620 TIF image using the Christoph Gohlke
tifffile code. A work in progress.

Created on Mon Aug 18 15:47:33 2014

@author: John Minter
"""

import os
import tifffile
import matplotlib.pyplot as plt
import skimage.io as io
import string

home=os.environ['HOME']
imgRoot=os.environ['IMG_ROOT']

relImg  = "/test/suite/"
# n.b. 17.56 and 17.57 scale X and Y by analySIS Five.
fName = 'fib620.tif'
filePath = imgRoot + relImg + fName

print(filePath)
tif = tifffile.TiffFile(filePath)
im = tif[0].asarray()

io.imshow(im, cmap=plt.cm.gray)
plt.show()

det = 0
mag = 0.0
ht = 0.0
fwd = 0.0
cap = ""

for page in tif:
  for tag in page.tags.values():
    t = tag.name, tag.value
    # what I want is in tag 34680
    if(tag.name == '34680'):
      myStr = tag.value.decode()
      ary = myStr.split('\r\n')
      for i in range(len(ary)):
        tst = ary[i].split(" = ")
        if( tst[0] == "lDetName"):
          det = int(tst[1])
        if( tst[0] == "Magnification"):
          mag = float(tst[1])
        if( tst[0] == "HighTension"):
          ht = float(tst[1])/1000.
        if( tst[0] == "FWD"):
          fwd = float(tst[1])
        if( tst[0] == "szUserText"):
          cap = str(tst[1])
        # print(ary[i])
print(det, mag, ht, fwd, cap)
      
