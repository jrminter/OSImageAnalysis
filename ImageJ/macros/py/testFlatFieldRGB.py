# flatFieldCorrect2.py
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-26  JRM 0.1.00  Test function in jmFijiGen.py


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
import jmFijiGen as jmg

impImg = IJ.openImage("D:\\Data\\eds\\Oxford\\QM14-04-04E-Steele\\reports\\BX61\\qm-04229-49U003-922-Row-2-Bus-Line\\qm-04229-efi-20X-1.tif")
impFF  = IJ.openImage("D:\\Data\\eds\\Oxford\\QM14-04-04E-Steele\\reports\\BX61\\qm-04229-49U003-922-Row-2-Bus-Line\\qm-04229-20x-1p6-col-pap-shade.tif")

impCor = jmg.flatFieldCorrectRGB(impImg, impFF, sigma=100)
impCor.show()