# test from Hadrian Mary
# needs 
# It's working for me now, as of the latest SCIFIO[1] and SCIFIO-OME-XML[2].
# Note that these libraries have updated dependencies compared to what's
# currently on Fiji, so you can't just drop these .jars into your Fiji
# installation if you want to test locally; you need to update the
# dependencies as well. The easiest way to do this would be to just clone
# Imagej.git[3] and install it into your Fiji.app directory by running:
#
# mvn -Dimagej.app.directory=/path/to/Fiji.app/ -Ddelete.other.versions=true
#
# We'll push these changes up to Fiji this week, and I will find or write
# better instructions for local testing.
#
from ij import IJ
from ij import ImagePlus
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os

from io.scif import SCIFIO
from io.scif.config import SCIFIOConfig
from io.scif.img import ImageRegion
from io.scif.img import ImgOpener
from io.scif.img import ImgSaver
from net.imagej.axis import Axes

imgDir  = os.environ['IMG_ROOT']
relImg  = "/test/original-ome"

inImg = imgDir + relImg + ".tif"
ouImg = imgDir + relImg + "-cr.tif"


axes = [Axes.X, Axes.Y]
ranges = ["%i-%i" % (2, 15), "%i-%i" % (2, 25)]
config = SCIFIOConfig()
config.imgOpenerSetRegion(ImageRegion(axes, ranges))

opener = ImgOpener()
imps = opener.openImgs(inImg, config)
imp = imps[0]

saver = ImgSaver()
saver.saveImg(ouImg, imp)

print('Done')