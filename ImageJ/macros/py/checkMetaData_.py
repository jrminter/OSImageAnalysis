# checkMetaData_.py
#
# see http://www.openmicroscopy.org/site/support/bio-formats5/users/imagej/index.html#macros-and-plugins
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-08-15  JRM 0.1.00  initial prototype development. Check image
#                         metadata
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from loci.formats.tiff import TiffParser
from loci.formats.in import SISReader
from loci.formats import ImageReader
from loci.formats import MetadataTools
from loci.plugins.util import LociPrefs
from loci.plugins.util import ImageProcessorReader
from loci.formats import ChannelSeparator
from ij import ImageStack
from ij import ImagePlus
from ij import IJ
import os

imgDir = os.environ['IMG_ROOT']
relImg  = "/test/suite/"

# n.b. 17.56 and 17.57 - this gets it wrong both 24.3889
fName = 'fib620.tif'
# fName = 'anaFiveDM.tif'
# fName = 'sirionSisBSE.tif'
# fName = 'sirionXHD.tif'
# fName = 'clumpedAgX.dm3'
filePath = imgDir + relImg + fName

r = ImageProcessorReader(ChannelSeparator(LociPrefs.makeImageReader()))
# print(dir(r))
r.setId(filePath)
num = r.getImageCount()
width = r.getSizeX()
height = r.getSizeY()
md = r.getGlobalMetadata()
# print(type(md))
# print(num, width, height)
stack = ImageStack(width, height)
i = 0
ip = r.openProcessors(i)[0]
stack.addSlice("1", ip);
imp = ImagePlus("foo", stack);
r.close()
imp.show()
IJ.run("Enhance Contrast", "saturated=0.35")

imageReader = ImageReader()
meta = MetadataTools.createOMEXMLMetadata()
imageReader.setMetadataStore(meta)
imageReader.setId(filePath)
pSizeX = meta.getPixelsPhysicalSizeX(0)
pSizeY = meta.getPixelsPhysicalSizeY(0)
imageReader.close()
print(pSizeX, pSizeY)
print(meta.getPixelsSizeX(0))
print(meta.getPixelsSizeY(0))






