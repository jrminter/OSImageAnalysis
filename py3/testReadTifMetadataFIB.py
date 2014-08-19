# -*- coding: utf-8 -*-
"""
testReadTifMetadataFIB.py

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
bIonBeam = True
bVerbose = False

relImg  = "/test/suite/"
# e-beam
# n.b. 17.56 and 17.57 scale X and Y by analySIS Five.

# ion beam
# n.b. 17.56 and 17.57 scale X and Y by analySIS Five.
# doesn't distinguish e-beam and ion beam

if bIonBeam:
  fName = 'fib620ib'
else:
  fName = 'fib620eb' 
  
filePath = imgRoot + relImg + fName + '.tif'

print(filePath)
tif = tifffile.TiffFile(filePath)
im = tif[0].asarray()

io.imshow(im, cmap=plt.cm.gray)
plt.show()

det = 0
mag = 0.0
ht = 0.0
iv = 0.0
fwd = 0.0
ss = 0
cap = ""

# an ini file for the image
filePath = imgRoot + relImg + fName + '.ini'
f = open(filePath, 'w')

for page in tif:
  for tag in page.tags.values():
    t = tag.name, tag.value
    # what I want is in tag 34680
    if(tag.name == '34680'):
      myStr = tag.value.decode()
      ary = myStr.split('\r\n')
      for i in range(len(ary)):
        strLine = "%s" % ary[i] + "\n"
        if (i > 0):
          f.write(strLine) 
        tst = ary[i].split(" = ")
        # in [DatabarData]
        # iImageType = 1 -> electron beam
        # iImageType = 2 -> ion beam
        if( tst[0] == "iImageType"):
          det = int(tst[1])
        if( tst[0] == "ProbeCurrent"):
          ss = int(float(tst[1]))
        if( tst[0] == "Magnification"):
          mag = float(tst[1])
        if( tst[0] == "flIonAccV"):
          iv = float(tst[1])/1000.
        if( tst[0] == "HighTension"):
          ht = float(tst[1])/1000.
        if( tst[0] == "FWD"):
          fwd = float(tst[1])
        if( tst[0] == "szUserText"):
          cap = str(tst[1])
        if bVerbose:
          print(ary[i])
f.close()          
print(det, mag, ht, iv, fwd, ss, cap)
      

  