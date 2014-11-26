from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
from ij import IJ
import jmFijiGen as jmg

imp = IJ.getImage()
imp = jmg.whiteBalance(imp)
imp.show()
