# EDF simple example
# from
# http://cmci.embl.de/documents/120206pyip_cooking/python_imagej_cookbook#pluginextended_depth_of_field_easy_mode
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-19  JRM 0.1.00  copied from source with minor adaptations
# 2014-10-21  JRM 0.1.10  added timing loop and contrast stretching
#                         added a crop boundary delta in case alignment
#                         is not perfect                         
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
from ij import ImagePlus
from ij import WindowManager

import time
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
w = imp.getWidth()
h = imp.getHeight()
imagesize = jarray.array([w, h], 'i')
color = imp.getType() == ImagePlus.COLOR_RGB
dl = BasicDialog(imagesize, color, False)
#  "quality='1' topology='0' show-view='on' show-topology='off'"
delta = 0
quality = 1
topology = 0
showview = True
showtopology= False
dl.parameters.setQualitySettings(quality)
dl.parameters.setTopologySettings(topology)
dl.parameters.show3dView = showview 
dl.parameters.showTopology = showtopology
dl.process()
while (WindowManager.getWindow("Output") is None ):
  time.sleep(1)
impEDF = WindowManager.getCurrentImage()
impEDF.show()
IJ.makeRectangle(delta, delta, w-2*delta, h-2*delta)
IJ.run("Crop")
IJ.run("Enhance Contrast", "saturated=0.0")
