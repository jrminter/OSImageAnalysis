# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:02:45 2015

@author: jrminter
"""
import numpy as np
from mayavi import mlab

x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
s = np.sin(x*y*z)/(x*y*z)

mlab.contour3d(s)

