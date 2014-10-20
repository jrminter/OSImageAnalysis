# EDF simple example
# from
# http://cmci.embl.de/documents/120206pyip_cooking/python_imagej_cookbook#pluginextended_depth_of_field_easy_mode
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-19  JRM 0.1.00  copied from source with minor adaptations
#                         TO DO: figure out expert mode from exemplar
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import jarray
from edfgui import BasicDialog
 
imp = IJ.getImage()
'''
here need to check conditions of the image, it should not be less than 
- 4 pixel width
- 4 pixel height
- 2 slices
'''
# should first par be width?
imagesize = jarray.array([imp.getHeight(), imp.getHeight()], 'i')
color = imp.getType() == ImagePlus.COLOR_RGB
dl = BasicDialog(imagesize, color, False)
#  "quality='1' topology='0' show-view='on' show-topology='off'"
quality = 1
topology = 0
showview = True
showtopology= False
dl.parameters.setQualitySettings(quality)
dl.parameters.setTopologySettings(topology)
dl.parameters.show3dView = showview 
dl.parameters.showTopology = showtopology
dl.process()