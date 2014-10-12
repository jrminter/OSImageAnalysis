# makeSimpleMontage_.py
#
# Make a montage from a list of files
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-11  JRM 0.1.00  Test makeMontage in jmFijiGen
#                         Use stainless Steel map

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import jmFijiGen as jmg

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images/map/png"
inDir  = gitDir + relImg
# Note: this fills row by row
lNames  = ["1-CK","2-AlK","3-SiK","4-CrK","5-MnK","6-FeK","7-NiK","8-MoK","9-ROI"]

#        sz   w-px  um
lCal = [67.9, 512, -6]
#       x0  y0  w   h
lCr  = [100,100,300,250]

impMont = jmg.makeMontage(lNames, 3, 3, inDir, lCal=lCal, lCr=lCr, sca=1.0)
impMont.show()

