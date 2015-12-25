# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 02:41:37 2015

@author: jrminter
"""

import os
import exifread
gitDir = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/noz-with-Fiji-metadata.tif"

fn = gitDir + relImg
f = open(fn, 'rb')

# Return Exif tags
tags = exifread.process_file(f)

print(tags)

