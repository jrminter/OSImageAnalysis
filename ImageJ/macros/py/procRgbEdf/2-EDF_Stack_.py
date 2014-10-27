# 2-EDF_Stack_.py
# adapted from from
# http://cmci.embl.de/documents/120206pyip_cooking/python_imagej_cookbook#pluginextended_depth_of_field_easy_mode
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-19  JRM 0.1.00  copied from source with minor adaptations
# 2014-10-21  JRM 0.1.10  added timing loop and contrast stretching
#                         could crop off a boundary delta in case alignment
#                         is not perfect                         
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import time
import jarray

from ij import IJ
from ij import ImagePlus
from ij import WindowManager

from edfgui import BasicDialog

# 1. Open an image and it's flat field
imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/efi-test/bez-50X-1"
strImg = imgDir + relImg + "/out/bez-50X-1-ij.tif"
print(strImg)
imp = IJ.openImage(strImg)
imp.show()

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

imp.close()
imp.flush()
strImg = imgDir + relImg + "/out/bez-50X-1-ij-edf.tif"
print(strImg)
IJ.saveAs("Tiff", strImg)

