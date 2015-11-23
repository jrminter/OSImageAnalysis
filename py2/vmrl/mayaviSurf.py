# -*- coding: utf-8 -*-
"""
mayaviSurf.py

Adapted from
http://scipy-cookbook.readthedocs.org/items/MayaVi_Surf.html

@author: l837410
"""

import numpy
def f(x, y):
    return numpy.sin(x*y)/(x*y)
x = numpy.arange(-7., 7.05, 0.1)
y = numpy.arange(-5., 5.05, 0.05)
from tvtk.tools import mlab
s = mlab.SurfRegular(x, y, f)
from mayavi.sources.vtk_data_source import VTKDataSource
d = VTKDataSource()
d.data = s.data

from mayavi.api import Engine
e = Engine()
e.start()
s = e.new_scene()

e.add_source(d)
from mayavi.filters.warp_scalar import WarpScalar
w = WarpScalar()
e.add_filter(w)
from mayavi.modules.outline import Outline
from mayavi.modules.surface import Surface
ou = Outline()
su = Surface()
e.add_module(ou)
e.add_module(su)