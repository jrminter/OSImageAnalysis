# 1-MakeStackFromDir_
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-27  JRM 0.1.00  Make a stack from a series of input images for
#                         processing to an EDF
#         
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import jmFijiGen as jmg
import os
from time import sleep
from ij import IJ

imgDir  = os.environ['IMG_ROOT']
relDir  = "/test/efi-test/bez-50X-1"

inpDir = imgDir + relDir + "/steps"

myImp = jmg.makeStackFromDir(inpDir, inExt='.tif', bDebug=False)

strImg = imgDir + relDir + "/out/bez-50X-1-ij.tif"
IJ.saveAs("Tiff", strImg)

sleep(2)
myImp.close()
myImp.flush()

