# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:28:09 2015

@author: l837410
"""
import os
from mayavi.sources.vrml_importer import VRMLImporter, View
from mayavi.api import Engine

gitDir = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images/vrml/"
fName = 'tree'

filePath = gitDir + relImg + fName +  '.wrl'
print(filePath)

e = Engine()
e.start()
s = e.new_scene()
src = VRMLImporter()
src.initialize(filePath)

# src.print_traits() # [0].mapper.input.points.to_array()
e.add_source(src)






