# -*- coding: utf-8 -*-
"""
testReadTifMetadataSirion.py

Read the metadata from an Sirion TIF image using the Christoph Gohlke
tifffile code. A work in progress.

Created   JRM 2014-08-18
Modified  JRM 2014-10-10 Move images into test suite dir. Note neither
                         read the metadata corectly. Grrrr....
          JRM 2015-12-23 Modified to get TiffFile from skimage

@author: John Minter
"""

import os
from skimage.external.tifffile import TiffFile #, imsave
from skimage.io import imshow 
import matplotlib.pyplot as plt
# import string


gitDir = os.environ['GIT_HOME']
bXHD = True
bVerbose = False

relImg  = "/OSImageAnalysis/images/suite/"

if bXHD:
  fName = 'sirionXHD'
else:
  fName = 'sirionSisBSE' 
  
filePath = gitDir + relImg + fName + '.tif'

print(filePath)
tif = TiffFile(filePath)
im = tif[0].asarray()

imshow(im, cmap=plt.cm.gray)
plt.show()

det = 0
mag = 0.0
ht = 0.0
iv = 0.0
fwd = 0.0
ss = 0
cap = ""

# an ini file for the image
filePath = gitDir + relImg + fName + '.ini'
f = open(filePath, 'w')

for page in tif:
  for tag in page.tags.values():
    t = tag.name, tag.value
    if bVerbose:
        print(tag.name)
        print(tag.value)
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
      

  