# -*- coding: utf-8 -*-
"""
displayCube.py

Display a VMR file of a cube

Created   JRM 2015-11-23

@author: John Minter
"""

import os
import mayavi
from mayavi.sources.vrml_importer import VRMLImporter
from mayavi.api import Engine


def show_vrml(fname):
    """Given a VRML file name it imports it into the scene.
	"""
	r = VRMLImporter()
	r.initialize(fname)
	eng.add_source(r)
	return r

gitDir = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/vrml/"

filePath = gitDir + relImg + 'cube.wrl'

print(filePath)






