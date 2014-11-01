# testHeadlessCrop_.py
#
# load and crop an image in headless mode
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
from ij.io import FileSaver

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images"
imgPath = gitDir + relImg + "/latex.tif"

delta = 32
imp = IJ.openImage(imgPath)
name = imp.getShortTitle()
w = imp.getWidth()
h = imp.getHeight()
imp.setRoi(delta,delta,w-(2*delta),h-(2*delta))
IJ.run(imp,"Crop","")

imgPath = gitDir + relImg + "/%s-cr.tif" % name

fs = FileSaver(imp) 
fs.saveAsTiff(imgPath) 



