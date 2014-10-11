# makeSimpleMontage_.py
#
# Make a montage from a list of files
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-11  JRM 0.1.00  Test makeMontage in jmFijiGen

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os
import glob
import time
from ij import IJ
from ij import ImagePlus
from ij import WindowManager
from io.scif.img import ImgOpener
import jmFijiGen as jmg

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images/map/png"
inDir  = gitDir + relImg
lNames  = ["2-OK","3-CuL","4-PK","5-PdL","6-AgL","7-ROI"]

lCal = [1.45, 512, -6]
# lCal=[]

impMont = jmg.makeMontage(lNames, 3, 2, inDir, lCal=lCal, sca=1.0)
# impMont = jmg.calibAZtecImage(impMont, 1.45, 512)
impMont.show()


  

