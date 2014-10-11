# ij2Ex_.py
#
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  ----------------------------------------------------
# 2014-10-03  JRM 0.1.00  Initial example. Used ideas from http://imglib2.net/
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from java.io import File
from ij import ImageJ, ImagePlus
from ij.io import Opener
from net.imglib2.img import Img, ImgFactory
from net.imglib2.img.cell import CellImgFactory
from net.imglib2.img.display.imagej import ImageJFunctions
from net.imglib2.type.numeric.real import FloatType



gitDir  = os.environ['GIT_HOME']
relImg  = "/OSImageAnalysis/images"
# strImg  = gitDir + relImg + "/bridge.gif"
strImg  = gitDir + relImg + "/latex.tif"

fi = File(strImg)
imp = Opener().openImage( fi.getAbsolutePath() )
imp.show()

imgFactory = CellImgFactory(5 )
img1 = imgFactory.create( (20, 30, 40), FloatType() )
ImageJFunctions.show( img1 )
img2 = imgFactory.create( img1, img1.firstElement() )
ImageJFunctions.show( img2 )


