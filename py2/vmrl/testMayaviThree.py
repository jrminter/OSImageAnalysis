# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:02:45 2015

@author: jrminter
"""
import numpy as np
from mayavi import mlab

x, y, z = np.mgrid[0:1:20j, 0:1:20j, 0:1:20j]

u =    np.sin(np.pi*x) * np.cos(np.pi*z)
v = -2*np.sin(np.pi*y) * np.cos(2*np.pi*z)
w = np.cos(np.pi*x)*np.sin(np.pi*z) + np.cos(np.pi*y)*np.sin(2*np.pi*z)

mlab.quiver3d(u, v, w)
mlab.outline()

