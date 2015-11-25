# -*- coding: utf-8 -*-
"""
displayVmrl.py

Display a VMR file of a cube

Created   JRM 2015-11-24

Do "%gui qt" first

@author: John Minter
"""

import os
from mayavi.sources.vrml_importer import VRMLImporter
from mayavi.api import Engine


gitDir = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/vrml/"
fName = 'Lines'

filePath = gitDir + relImg + fName + '.wrl'
print(filePath)

e = Engine()
e.start()
s = e.new_scene()
src = VRMLImporter()
src.initialize(filePath)
e.add_source(src)
