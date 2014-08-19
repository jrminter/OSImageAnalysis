# -*- coding: utf-8 -*-
"""
testReadTifMetadataAnaPC.py

Read the metadata from an TIF image recorded using the analySIS PC on
the Sirion with analySIS 5.0   using the Christoph Gohlke tifffile code.

A work in progress.

Created on Mon Aug 19 9:25:33 2014

@author: John Minter
"""

import os
import tifffile
import matplotlib.pyplot as plt
import skimage.io as io
import string

home=os.environ['HOME']
imgRoot=os.environ['IMG_ROOT']
bVerbose = False

relImg  = "/test/suite/"

fName = 'sirionXHD' 
  
filePath = imgRoot + relImg + fName + '.tif'

print(filePath)
tif = tifffile.TiffFile(filePath)
im = tif[0].asarray()

io.imshow(im, cmap=plt.cm.gray)
plt.show()

for page in tif:
  for tag in page.tags.values():
    t = tag.name, tag.value
    # what I want is in tag 34680
    print(t)
    if(tag.name == '33560'):
      myStr = tag.value.decode()
      ary = myStr.split('\r\n')
      for i in range(len(ary)):
        print(ary[i])

