# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 15:47:33 2014

@author: l837410
"""

import os
import tifffile
home=os.environ['HOME']
imgRoot=os.environ['IMG_ROOT']

relImg  = "/test/suite/"
# n.b. 17.56 and 17.57 - this gets it wrong both 24.3889
fName = 'fib620.tif'
filePath = imgRoot + relImg + fName

print(filePath)